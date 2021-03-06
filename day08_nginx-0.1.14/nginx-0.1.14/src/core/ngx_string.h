
/*
 * Copyright (C) Igor Sysoev
 */


#ifndef _NGX_STRING_H_INCLUDED_
#define _NGX_STRING_H_INCLUDED_


#include <ngx_config.h>
#include <ngx_core.h>


typedef struct {
    size_t    len;
    u_char   *data;
} ngx_str_t;


#define ngx_string(str)  { sizeof(str) - 1, (u_char *) str }
#define ngx_null_string  { 0, NULL }


#define ngx_tolower(c)     (u_char) ((c >= 'A' && c <= 'Z') ? (c | 0x20) : c)


#if (NGX_WIN32)

#define ngx_strncasecmp(s1, s2, n)                                           \
                           strnicmp((const char *) s1, (const char *) s2, n)
#define ngx_strcasecmp(s1, s2)                                               \
                           stricmp((const char *) s1, (const char *) s2)

#else

#define ngx_strncasecmp(s1, s2, n)                                           \
                           strncasecmp((const char *) s1, (const char *) s2, n)
#define ngx_strcasecmp(s1, s2)                                               \
                           strcasecmp((const char *) s1, (const char *) s2)

#endif


#define ngx_strncmp(s1, s2, n)  strncmp((const char *) s1, (const char *) s2, n)


/* msvc and icc compile strcmp() to inline loop */
#define ngx_strcmp(s1, s2)  strcmp((const char *) s1, (const char *) s2)


#define ngx_strstr(s1, s2)  strstr((const char *) s1, (const char *) s2)
#define ngx_strlen(s)       strlen((const char *) s)


/*
 * msvc and icc compile memset() to the inline "rep stos"
 * while ZeroMemory() and bzero() are the calls.
 * icc may also inline several mov's of a zeroed register for small blocks.
 */
#define ngx_memzero(buf, n)       memset(buf, 0, n)
#define ngx_memset(buf, c, n)     memset(buf, c, n)


/* msvc and icc compile memcpy() to the inline "rep movs" */
#define ngx_memcpy(dst, src, n)   memcpy(dst, src, n)
#define ngx_cpymem(dst, src, n)   ((u_char *) memcpy(dst, src, n)) + (n)


/* msvc and icc compile memcmp() to the inline loop */
#define ngx_memcmp                memcmp


u_char *ngx_cpystrn(u_char *dst, u_char *src, size_t n);
u_char *ngx_sprintf(u_char *buf, const char *fmt, ...);
u_char *ngx_snprintf(u_char *buf, size_t max, const char *fmt, ...);
u_char *ngx_vsnprintf(u_char *buf, size_t max, const char *fmt, va_list args);

ngx_int_t ngx_rstrncmp(u_char *s1, u_char *s2, size_t n);
ngx_int_t ngx_rstrncasecmp(u_char *s1, u_char *s2, size_t n);

ngx_int_t ngx_atoi(u_char *line, size_t n);
ngx_int_t ngx_hextoi(u_char *line, size_t n);

void ngx_md5_text(u_char *text, u_char *md5);


#define ngx_base64_encoded_length(len)  (((len + 2) / 3) * 4)
#define ngx_base64_decoded_length(len)  (((len + 3) / 4) * 3)

void ngx_encode_base64(ngx_str_t *dst, ngx_str_t *src);
ngx_int_t ngx_decode_base64(ngx_str_t *dst, ngx_str_t *src);


#define NGX_ESCAPE_URI   0
#define NGX_ESCAPE_HTML  1

ngx_uint_t ngx_escape_uri(u_char *dst, u_char *src, size_t size,
                          ngx_uint_t type);


#define  ngx_qsort                qsort


#define  ngx_value_helper(n)      #n
#define  ngx_value(n)             ngx_value_helper(n)


#endif /* _NGX_STRING_H_INCLUDED_ */
