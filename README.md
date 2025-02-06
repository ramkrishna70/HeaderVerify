# Security Header Verification API

## Overview
The Security Header Verification API helps evaluate security headers of a given URL and assigns scores based on best security practices. The API is built using Flask and provides an endpoint to check security headers.

## API Endpoint
**URL:** `https://header-verify.bithost.in/api/results`

**Method:** `POST`

**Content-Type:** `application/json`

## Example Request
Using `curl`:
```sh
curl --silent --location --request POST 'https://header-verify.bithost.in/api/results' \
--header 'Content-Type: application/json' \
--data '{
    "url": "https://bithost.in"
}'
```

## Example Response
```json
{
    "header_details": [
        {
            "header": "Strict-Transport-Security",
            "score": 10,
            "value": "max-age=2592000; includeSubDomains; preload"
        },
        {
            "header": "Content-Security-Policy",
            "score": 0,
            "value": "Not present"
        },
        {
            "header": "X-Content-Type-Options",
            "score": 6,
            "value": "nosniff"
        },
        {
            "header": "X-Frame-Options",
            "score": 5,
            "value": "SAMEORIGIN"
        },
        {
            "header": "X-XSS-Protection",
            "score": 5,
            "value": "1; mode=block"
        },
        {
            "header": "Referrer-Policy",
            "score": 5,
            "value": "same-origin"
        },
        {
            "header": "Permissions-Policy",
            "score": 4,
            "value": "accelerometer=(),autoplay=(),browsing-topics=(),camera=(),clipboard-read=(),clipboard-write=(),geolocation=(),gyroscope=(),hid=(),interest-cohort=(),magnetometer=(),microphone=(),payment=(),publickey-credentials-get=(),screen-wake-lock=(),serial=(),sync-xhr=(),usb=()"
        },
        {
            "header": "Cache-Control",
            "score": 6,
            "value": "private, max-age=0, no-store, no-cache, must-revalidate, post-check=0, pre-check=0"
        },
        {
            "header": "Expect-CT",
            "score": 7,
            "value": "max-age=86400, enforce"
        },
        {
            "header": "Public-Key-Pins",
            "score": 0,
            "value": "Not present"
        },
        {
            "header": "Cross-Origin-Resource-Policy",
            "score": 2,
            "value": "same-origin"
        },
        {
            "header": "Feature-Policy",
            "score": 0,
            "value": "Not present"
        },
        {
            "header": "Set-Cookie",
            "score": 0,
            "value": "Not present"
        },
        {
            "header": "Content-Type-Security-Policy",
            "score": 0,
            "value": "Not present"
        },
        {
            "header": "report-to",
            "score": 3,
            "value": "{\"endpoints\":[{\"url\":\"https:\\/\\/a.nel.cloudflare.com\\/report\\/v4?s=5vv%2FmvrRD2VvyW%2FaKN%2BUrT6Bv%2FyFIILxanwJeio7uwthKb6MjOKlnJDbG71C2EhIWP7RWZKYSyD2F6YII2OKmMF5ZYUTBxAxAiUpYwLPysT3270Fszv2GdYZ18bXlJbopQ%3D%3D\"}],\"group\":\"cf-nel\",\"max_age\":604800}"
        },
        {
            "header": "server",
            "score": 1,
            "value": "cloudflare"
        },
        {
            "header": "content-encoding",
            "score": 2,
            "value": "gzip"
        },
        {
            "header": "nel",
            "score": 1,
            "value": "{\"success_fraction\":0,\"report_to\":\"cf-nel\",\"max_age\":604800}"
        },
        {
            "header": "Cross-Origin-Embedder-Policy",
            "score": 2,
            "value": "require-corp"
        },
        {
            "header": "Cross-Origin-Opener-Policy",
            "score": 2,
            "value": "same-origin"
        },
        {
            "header": "Set-Cookie",
            "score": 0,
            "value": "Checked for Secure/HttpOnly flags"
        }
    ],
    "score": 61,
    "server_ip": "104.21.112.1",
    "total_headers": 20
}

```
 

## Security Headers Checked
- `Strict-Transport-Security`
- `Content-Security-Policy`
- `X-Content-Type-Options`
- `X-Frame-Options`
- `X-XSS-Protection`
- `Referrer-Policy`
- `Permissions-Policy`
- `Cache-Control`
- `Expect-CT`
- `Public-Key-Pins`
- `Cross-Origin-Resource-Policy`
- `Feature-Policy`
- `Set-Cookie`
- `Content-Type-Security-Policy`
- `report-to`
- `server`
- `content-encoding`
- `nel`
- `Cross-Origin-Embedder-Policy`
- `Cross-Origin-Opener-Policy`
- `Cross-Origin-Resource-Policy`

## License
This project is licensed under [MIT License](LICENSE).

## Contact
For any issues or feature requests, please contact [Zhost Consulting Private Limited](https://www.bithost.in/).

