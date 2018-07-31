# dns_update_cloudflare_api
A quick script to update my DNS records, when my public IP address changes.

You will need to create a json file somewhere with your Cloudflare credentials. Keep it protected, and out of the git repo.

```json
{
  "api_url" : "<cloudflares upi url>",
  "api_email" : "<your email address registered with your cloudflare account>",
  "api_key" : "<your cloudflare api key - KEEP THIS SAFE>",
  "zoneid" : "<The zone_id of your cloudflare managed domain.>",
  "ip_file" : "<Local file where your public ip address is maintained.>"
}
```
