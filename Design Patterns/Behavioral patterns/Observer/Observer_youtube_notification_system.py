'''

        Scenario
        You have a YouTube-like system:
        - A Channel uploads videos
        - Users (subscribers) should get notified

'''


# Observer Pattern = One-to-Many Event Notification System

"""
Publisher (Channel)
    ↓
Notifies
    ↓
Multiple Subscribers (Users, Services, Systems)

"""

'''
main idea of Observer Pattern is to decouple the publisher and subscribers. The publisher should not know about the subscribers. The subscribers should not know about the publisher. The publisher should only know about the interface of the subscribers. The subscribers should only know about the interface of the publisher.


Instead of pooling where the subscribers keep asking the publisher if there is any new video, the publisher should notify the subscribers when there is a new video. This is called "Event-driven" programming or push-based programming. The publisher pushes the event to the subscribers. The subscribers can then decide what to do with the event.

channel - event producer
subscriber - event consumer
'''

from abc import ABC, abstractmethod

# Subscriber Interface

class Subscriber(ABC):

    @abstractmethod
    def update(self):
        pass


# Channel/publisher Interface

class Channel(ABC):

    @abstractmethod
    def subscribe(self, subscriber: Subscriber):
        pass

    @abstractmethod
    def unsubscribe(self, subscriber: Subscriber):
        pass

    @abstractmethod
    def notify_subscribers(self):
        pass


# concrete channel/publisher class-subject class

class YouTubeChannel(Channel):

    def __init__(self, name: str):
        self.name = name
        self._subscribers: list[Subscriber] = []
        self._latest_video = None

    def subscribe(self, subscriber: Subscriber):
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber: Subscriber):
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)

    def notify_subscribers(self):
        for sub in self._subscribers:
            sub.update()

    def upload_video(self, title: str):
        self._latest_video = title
        print(f"\n[{self.name} uploaded '{title}']")
        self.notify_subscribers()

    def get_video_data(self):
        return f"Checkout our new video: {self._latest_video}"


# concrete subscriber class / Observer class

class UserSubscriber(Subscriber):

    def __init__(self, name: str, channel: YouTubeChannel):
        self.name = name
        self.channel = channel

    def update(self):
        print(f"Hey {self.name}, {self.channel.get_video_data()}")


#Client code

if __name__ == "__main__":

    # Create channel
    channel = YouTubeChannel("Brainopedia Gaming")

    # Create subscribers
    user1 = UserSubscriber("Mihir", channel)
    user2 = UserSubscriber("Moulik", channel)

    # Subscribe
    channel.subscribe(user1)
    channel.subscribe(user2)

    # Upload video
    channel.upload_video("Free Fire Gameplay push to Grandmaster")

    # Unsubscribe one user
    channel.unsubscribe(user1)

    # Upload another video
    channel.upload_video("PUBG Gameplay push to Conqueror")


  
'''
Output :

[Brainopedia Gaming uploaded 'Free Fire Gameplay push to Grandmaster']
Hey Mihir, Checkout our new video: Free Fire Gameplay push to Grandmaster
Hey Moulik, Checkout our new video: Free Fire Gameplay push to Grandmaster

[Brainopedia Gaming uploaded 'PUBG Gameplay push to Conqueror']
Hey Moulik, Checkout our new video: PUBG Gameplay push to Conqueror
'''

