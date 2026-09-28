'''
Problem Statement: 

        Scenario
        You have a YouTube-like system:
        - A Channel uploads videos
        - Users (subscribers) should get notified

'''

class Channel:
    def __init__(self, name):
        self.name = name
        self.latest_video = None

    def upload_video(self, title):
        self.latest_video = title
        print(f"\n[{self.name} uploaded '{title}']")

        # Hardcoded subscribers (BAD)
        self.notify_varun()
        self.notify_tarun()

    def notify_varun(self):
        print("Hey Varun, check out new video:", self.latest_video)

    def notify_tarun(self):
        print("Hey Tarun, check out new video:", self.latest_video)

# users are hardcoded in the Channel class, which is not scalable. - Tightly coupled. If we want to add more users, we have to modify the Channel class. This violates the Open/Closed Principle.

# What if 1M Subscribers are there?  -> maintainance nightmare.  -> We need to decouple the Channel and Users.  -> Observer Pattern



