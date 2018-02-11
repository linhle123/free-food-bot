# import json
# import getdata


# def getEventsCarousel(events):
#     elements = []
#     for event in events:
#         event = {
#             "title":event[0].encode('utf-8'),
#             "image_url":"https://www.google.com/",
#             "subtitle":event[1].strftime("%I:%M %p"),
#             "default_action": {
#                 "type": "web_url",
#                 "url": "https://www.quora.com/",
#                 "webview_height_ratio": "tall",
#                 "fallback_url": "https://www.google.com/"
#             },
#             "buttons":[
#                 {
#                     "type":"web_url",
#                     "url":"https://anchorlink.vanderbilt.edu"+event[4],
#                     "title":"Details",
#                     "webview_height_ratio": "compact",
#                 }          
#             ]      
#         }
#         elements.append(event)
#     return elements

# free_food_events = getdata.get_free_food_events()
# data = json.dumps(getEventsCarousel(free_food_events))

# print(data)
