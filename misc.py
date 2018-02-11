import json
# import getdata
import datetime

events = [[u'Temple Visit', datetime.datetime(2018, 2, 11, 11, 30), u'Sri Ganesha Temple', u'Spirituality', u'/event/1821402'], [u'BlackGirlFest', datetime.datetime(2018, 2, 11, 13, 0), u'Student Life Center', u'Social', u'/event/1355201'], [u'Tzedkah Tzunday', datetime.datetime(2018, 2, 11, 7, 0), u'Gordon Jewish Community Center', u'Service', u'/event/1670400'], [u'Social Justice, Gender and Legal Change in Asylum Law', datetime.datetime(2018, 2, 12, 12, 0), u'Vanderbilt Law School - Renaissance Room', u'Learning', u'/event/1773683'], [u'BCC TOWNHALL:  Male/Female Relationships @ BlackVU', datetime.datetime(2018, 2, 12, 18, 0), u'Black Cultural Center', u'Learning', u'/event/1797000'], [u'Mesa espa\xf1ola ', datetime.datetime(2018, 2, 13, 14, 0), u'Furman 001- Center for Second Language Studies', u'Cultural', u'/event/1788476'], [u'Women in Business Career Carnival', datetime.datetime(2018, 2, 13, 18, 0), u'Community Room in the Central Library (across from the Cafe)', u'Learning', u'/event/1800805'], [u'McGill Family Dinner', datetime.datetime(2018, 2, 13, 18, 0), u'McGill TV Lounge', u'Social', u'/event/1822821'], [u'Shivratri', datetime.datetime(2018, 2, 13, 18, 30), u'OUCRL', u'Spirituality', u'/event/1821327'], [u'Kaffeestunde', datetime.datetime(2018, 2, 14, 14, 30), u'Center for Second Language Studies - Furman 001', u'Cultural', u'/event/1757251'], [u'Brown Bag Cultural Heritage Month Showcase: Black History Month ', datetime.datetime(2018, 2, 15, 12, 0), u'SJI Lounge (Sarratt 335)', u'Cultural', u'/event/1760974'], [u'Dialogue Dinner', datetime.datetime(2018, 2, 15, 17, 30), u'Office of Religious Life', u'Spirituality', u'/event/1791925'], [u'"Micro-aggressions on the Wards" - A Student Led Discussion', datetime.datetime(2018, 2, 15, 17, 30), u'Light Hall 433', u'Learning', u'/event/1800626'], [u'Dinner without Borders', datetime.datetime(2018, 2, 15, 18, 0), u'Sarratt 216/220', u'Cultural', u'/event/1676937'], [u'QPOC Social', datetime.datetime(2018, 2, 15, 18, 0), u'Black Cultural Center', u'Social', u'/event/1806576'], [u'MannaFit', datetime.datetime(2018, 2, 15, 18, 0), u'Student Life Center Ballroom', u'Fundraising', u'/event/1677461'], [u'WCC First GBM', datetime.datetime(2018, 2, 15, 19, 0), u'Stevenson 2122', u'Service', u'/event/1829225'], [u"Mark Zuckerberg's War on Free Will: How Big Tech Threatens the Individual", datetime.datetime(2018, 2, 16, 12, 0), u'Flynn Auditorium ', u'Learning', u'/event/1806303'], [u'Financial Literacy: $mart Habits that $ave Money ', datetime.datetime(2018, 2, 16, 14, 0), u'Buttrick Hall 205 ', u'Learning', u'/event/1791863'], [u'Chapman Hosts Social Rounds!', datetime.datetime(2018, 2, 16, 17, 0), u'Student Lounge, Light Hall', u'Social', u'/event/1808712'], [u'The Big Event ', datetime.datetime(2018, 2, 17, 11, 0), u'Field House ', u'Fundraising', u'/event/1663633'], [u'Chinese New Year Celebration', datetime.datetime(2018, 2, 18, 17, 30), u'Alumni 202 and 206', u'Cultural', u'/event/1766820'], [u'Hella Safe Sex', datetime.datetime(2018, 2, 19, 11, 0), u'Sarratt 363', u'Social', u'/event/1745134'], [u'Student of Color Affinity Group', datetime.datetime(2018, 2, 19, 12, 0), u'SJI Lounge (Sarratt 335)', u'Cultural', u'/event/1767169'], [u'Black Panther Through A Comic Book Lens \u2022 Panel Discussion', datetime.datetime(2018, 2, 19, 12, 0), u'Black Cultural Center', u'Cultural', u'/event/1821272'], [u'Social Justice & the Legal Profession Series: Legal Aid Lawyering for Social Justice', datetime.datetime(2018, 2, 20, 12, 0), u'Vanderbilt Law School - Hyatt Room (#144)', u'Learning', u'/event/1813743'], [u'Mesa espa\xf1ola ', datetime.datetime(2018, 2, 20, 14, 0), u'Furman 001- Center for Second Language Studies', u'Cultural', u'/event/1788477'], [u'[IM]Perfection Project Speak-Out Panel ', datetime.datetime(2018, 2, 20, 19, 0), u'Alumni Hall 100 ', u'Learning', u'/event/1671450']]

print(len("hello"))
maxLen = 0
longest = ""
for event in events:
    if len(event[2]) > maxLen:
        maxLen = len(event[2])
        longest = event[2]

print(maxLen)
print(longest)
# def print_events_info(events):
#     for event in events:
#         event_info = "{}\nTime: {}\nLocation: {}\n".format(
#             event[0].encode('utf-8'),event[1].strftime("%I:%M %p"),event[2].encode('utf-8'))
#         print(event_info)

#each chunk has 10 event max, because carousel contain 10 items max
# chunks = [events[x:x+10] for x in xrange(0, len(events), 10)]
# print("there are {} events".format(len(events)))
# print("there are {} chunks".format(len(chunks)))
# print(chunks[2])

# def getEventsCarousel(events):
#     chunks = [events[x:x+10] for x in xrange(0, len(events), 10)]
#     event_groups = []
#     for chunk in chunks:
#         event_group = []
#         for event in chunk:
#             event_info = {
#                     "title":event[0].encode('utf-8'),
#                     "subtitle":event[1].strftime("%I:%M %p"),
#                     "buttons":[
#                         {
#                             "type":"web_url",
#                             "url":"https://anchorlink.vanderbilt.edu"+event[4],
#                             "title":"Details",
#                             "webview_height_ratio": "compact",
#                         }          
#                     ]      
#                 }
#             event_group.append(event_info)
#         event_groups.append(event_group)
#     return event_groups

# event_groups = getEventsCarousel(events)

# for event_group in event_groups:
#     print("this group has {} events".format(len(event_group)))
#     print(event_group)
