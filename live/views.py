from django.shortcuts import render
from django.http import JsonResponse
import requests

import json

API_KEY_SECRET = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiVTJGc2RHVmtYMS8ya1VGajFQWFcvMFB1QlBzT1Z2bytLdG5lQXUyTjBlb0FGQ1l6RXBIL3BlRmc2bWdXMHVDZjEzSEZ1SFNFWUl2U1ZMR3hPSFc2K1BrWHkzR1lkb2dISUVobTlsOUVEU3JLZlNJUkZUVEltd3pNRENHQncycDYiLCJpYXQiOjE3MTY4MTc0MjEsImV4cCI6MTcxNjgyNDYyMX0.s3uGtBeoHOmo-DPvSBZpieFeHDcuJO5GVmB0ogs_wJo"
# MIROTALK_URL = "https://sfu.mirotalk.com/api/v1/meeting"
MIROTALK_URL = "https://kidslive-5837dd19-0b67-429b-b2b9.renu-01.cranecloud.io/api/v1/meeting"

headers = {
    "authorization": API_KEY_SECRET,
    "Content-Type": "application/json",
}

def  video_conference(request):
    # Assuming MiroTalk requires an API call to create a new conference room
    response = requests.post(MIROTALK_URL, headers=headers, data={})
    res = response.json()
    if res.get("error") is None:
        room_data = res
        context = {
            'room_url': room_data['meeting'],
            # 'room_id': room_data['roomId'],
            # Include other necessary context variables
        }
        return render(request, 'live/conference.html', context)
    else:
        return JsonResponse(res["error"], status=401, safe=False)


