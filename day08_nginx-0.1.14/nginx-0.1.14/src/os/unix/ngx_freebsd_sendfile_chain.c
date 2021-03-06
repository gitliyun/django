
/*
 * Copyright (C) Igor Sysoev
 */


#include <ngx_config.h>
#include <ngx_core.h>
#include <ngx_event.h>


/*
 * Although FreeBSD sendfile() allows to pass a header and a trailer,
 * it can not send a header with a part of the file in one packet until
 * FreeBSD 5.3.  Besides, over the fast ethernet connection sendfile()
 * may send the partially filled packets, i.e. the 8 file pages may be sent
 * as the 11 full 1460-bytes packets, then one incomplete 324-bytes packet,
 * and then again the 11 full 1460-bytes packets.
 *
 * Threfore we use the TCP_NOPUSH option (similar to Linux's TCP_CORK)
 * to postpone the sending - it not only sends a header and the first part of
 * the file in one packet, but also sends the file pages in the full packets.
 *
 * But until FreeBSD 4.5 the turning TCP_NOPUSH off does not flush a pending
 * data that less than MSS so that data may be sent with 5 second delay.
 * So we do not use TCP_NOPUSH on FreeBSD prior to 4.5 although it can be used
 * for non-keepalive HTTP connections.
 */


#define NGX_HEADERS   8
#define NGX_TRAILERS  4


ngx_chain_t *ngx_freebsd_sendfile_chain(ngx_connection_t *c, ngx_chain_t *in,
                                        off_t limit)
{
    int              rc;
    u_char          *prev;
    off_t            size, send, prev_send, aligned, sent, fprev;
    size_t           header_size, file_size;
    ngx_uint_t       eintr, eagain, complete;
    ngx_err_t        err;
    ngx_buf_t       *file;
    ngx_array_t      header, trailer;
    ngx_event_t     *wev;
    ngx_chain_t     *cl;
    struct sf_hdtr   hdtr;
    struct iovec    *iov, headers[NGX_HEADERS], trailers[NGX_TRAILERS];

    wev = c->write;

    if (!wev->ready) {
        return in;
    }

#if (NGX_HAVE_KQUEUE)

    if ((ngx_event_flags & NGX_USE_KQUEUE_EVENT) && wev->pending_eof) {
        ngx_log_error(NGX_LOG_INFO, c->log, wev->kq_errno,
                      "kevent() reported about an closed connection");

        wev->error = 1;
        return NGX_CHAIN_ERROR;
    }

#endif

    /* the maximum limit size is the maximum size_t value - the page size */

    if (limit == 0 || limit > NGX_MAX_SIZE_T_VALUE - ngx_pagesize) {
        limit = NGX_MAX_SIZE_T_VALUE - ngx_pagesize;
    }

    send = 0;
    eagain = 0;

    header.elts = headers;
    header.size = sizeof(struct iovec);
    header.nalloc = NGX_HEADERS;
    header.pool = c->pool;

    trailer.elts = trailers;
    trailer.size = sizeof(struct iovec);
    trailer.nalloc = NGX_TRAILERS;
    trailer.pool = c->pool;

    for ( ;; ) {
        file = NULL;
        file_size = 0;
        header_size = 0;
        eintr = 0;
        complete = 0;
        prev_send = send;

        header.nelts = 0;
        trailer.nelts = 0;

        /* create the header iovec and coalesce the neighbouring bufs */

        prev = NULL;
        iov = NULL;

        for (cl = in;
             cl && header.nelts < IOV_MAX && send < limit;
             cl = cl->next)
        {
            if (ngx_buf_special(cl->buf)) {
                continue;
            }

            if (!ngx_buf_in_memory_only(cl->buf)) {
                break;
            }

            size = cl->buf->last - cl->buf->pos;

            if (send + size > limit) {
                size = limit - send;
            }

            if (prev == cl->buf->pos) {
                iov->iov_len += (size_t) size;

            } else {
                if (!(iov = ngx_array_push(&header))) {
                    return NGX_CHAIN_ERROR;
                }

                iov->iov_base = (void *) cl->buf->pos;
                iov->iov_len = (size_t) size;
            }

            prev = cl->buf->pos + (size_t) size;
            header_size += (size_t) size;
            send += size;
        }


        if (cl && cl->buf->in_file && send < limit) {
            file = cl->buf;

            /* coalesce the neighbouring file bufs */

            do {
                size = cl->buf->file_last - cl->buf->file_pos;

                if (send + size > limit) {
                    size = limit - send;

                    aligned = (cl->buf->file_pos + size + ngx_pagesize - 1)
                                                      & ~(ngx_pagesize - 1);

                    if (aligned <= cl->buf->file_last) {
                        size = aligned - cl->buf->file_pos;
                    }
                }

                file_size += (size_t) size;
                send += size;
                fprev = cl->buf->file_pos + size;
                cl = cl->next;

            } while (cl
                     && cl->buf->in_file
                     && send < limit
                     && file->file->fd == cl->buf->file->fd
                     && fprev == cl->buf->file_pos);
        }


        if (file) {

            /* create the tailer iovec and coalesce the neighbouring bufs */

            prev = NULL;
            iov = NULL;

            while (cl && header.nelts < IOV_MAX && send < limit) {

                if (ngx_buf_special(cl->buf)) {
                    cl = cl->next;
                    continue;
                }

                if (!ngx_buf_in_memory_only(cl->buf)) {
                    break;
                }

                size = cl->buf->last - cl->buf->pos;

                if (send + size > limit) {
                    size = limit - send;
                }

                if (prev == cl->buf->pos) {
                    iov->iov_len += (size_t) size;

                } else {
                    if (!(iov = ngx_array_push(&trailer))) {
                        return NGX_CHAIN_ERROR;
                    }

                    iov->iov_base = (void *) cl->buf->pos;
                    iov->iov_len = (size_t) size;
                }

                prev = cl->buf->pos + (size_t) size;
                send += size;
                cl = cl->next;
            }
        }

        if (file) {

            if (ngx_freebsd_use_tcp_nopush
                && c->tcp_nopush == NGX_TCP_NOPUSH_UNSET)
            {
                if (ngx_tcp_nopush(c->fd) == NGX_ERROR) {
                    err = ngx_errno;

                    /*
                     * there is a tiny chance to be interrupted, however,
                     * we continue a processing without the TCP_NOPUSH
                     */

                    if (err != NGX_EINTR) {
                        wev->error = 1;
                        ngx_connection_error(c, err,
                                             ngx_tcp_nopush_n " failed");
                        return NGX_CHAIN_ERROR;
                    }

                } else {
                    c->tcp_nopush = NGX_TCP_NOPUSH_SET;

                    ngx_log_debug0(NGX_LOG_DEBUG_EVENT, c->log, 0,
                                   "tcp_nopush");
                }
            }

            hdtr.headers = (struct iovec *) header.elts;
            hdtr.hdr_cnt = header.nelts;
            hdtr.trailers = (struct iovec *) trailer.elts;
            hdtr.trl_cnt = trailer.nelts;

            /*
             * the "nbytes bug" of the old sendfile() syscall:
             * http://www.freebsd.org/cgi/query-pr.cgi?pr=33771
             */

            if (!ngx_freebsd_sendfile_nbytes_bug) {
                header_size = 0;
            }

            sent = 0;

            rc = sendfile(file->file->fd, c->fd, file->file_pos,
                          file_size + header_size, &hdtr, &sent, 0);

            if (rc == -1) {
                err = ngx_errno;

                if (err == NGX_EAGAIN || err == NGX_EINTR) {
                    if (err == NGX_EINTR) {
                        eintr = 1;

                    } else {
                        eagain = 1;
                    }

                    ngx_log_debug1(NGX_LOG_DEBUG_EVENT, c->log, err,
                                   "sendfile() sent only %O bytes", sent);

                } else {
                    wev->error = 1;
                    ngx_connection_error(c, err, "sendfile() failed");
                    return NGX_CHAIN_ERROR;
                }
            }

            if (rc == 0 && sent == 0) {

                /*
                 * rc and sent equal to zero when someone has truncated
                 * the file, so the offset became beyond the end of the file
                 */

                ngx_log_error(NGX_LOG_ALERT, c->log, 0,
                              "sendfile() reported that \"%s\" was truncated",
                              file->file->name.data);

                return NGX_CHAIN_ERROR;
            }

            ngx_log_debug4(NGX_LOG_DEBUG_EVENT, c->log, 0,
                           "sendfile: %d, @%O %O:%uz",
                           rc, file->file_pos, sent, file_size + header_size);

        } else {
            rc = writev(c->fd, header.elts, header.nelts);

            ngx_log_debug2(NGX_LOG_DEBUG_EVENT, c->log, 0,
                           "writev: %d of %uz", rc, header_size);

            if (rc == -1) {
                err = ngx_errno;

                if (err == NGX_EAGAIN || err == NGX_EINTR) {
                    if (err == NGX_EINTR) {
                        eintr = 1;
                    }

                    ngx_log_debug0(NGX_LOG_DEBUG_EVENT, c->log, err,
                                   "writev() not ready");

                } else {
                    wev->error = 1;
                    ngx_connection_error(c, err, "writev() failed");
                    return NGX_CHAIN_ERROR;
                }
            }

            sent = rc > 0 ? rc : 0;
        }

        if (send - prev_send == sent) {
            complete = 1;
        }

        c->sent += sent;

        for (cl = in; cl; cl = cl->next) {

            if (ngx_buf_special(cl->buf)) {
                continue;
            }

            if (sent == 0) {
                break;
            }

            size = ngx_buf_size(cl->buf);

            if (sent >= size) {
                sent -= size;

                if (ngx_buf_in_memory(cl->buf)) {
                    cl->buf->pos = cl->buf->last;
                }

                if (cl->buf->in_file) {
                    cl->buf->file_pos = cl->buf->file_last;
                }

                continue;
            }

            if (ngx_buf_in_memory(cl->buf)) {
                cl->buf->pos += (size_t) sent;
            }

            if (cl->buf->in_file) {
                cl->buf->file_pos += sent;
            }

            break;
        }

        if (eagain) {

            /*
             * sendfile() may return EAGAIN, even if it has sent a whole file
             * part, it indicates that the successive sendfile() call would
             * return EAGAIN right away and would not send anything.
             * We use it as a hint.
             */

            wev->ready = 0;
            return cl;
        }

        if (eintr) {
            continue;
        }

        if (!complete) {
            wev->ready = 0;
            return cl;
        }

        if (send >= limit || cl == NULL) {
            return cl;
        }

        in = cl;
    }
}
