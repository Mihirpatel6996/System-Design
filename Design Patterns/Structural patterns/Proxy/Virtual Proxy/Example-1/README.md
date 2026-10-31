1. What is a Virtual Proxy (Real Meaning)
A Virtual Proxy is used when:
Creating a real object is expensive, but you don’t always need it.

So instead of creating it upfront, you:
- Delay creation
- Only create it when actually required
Real-world analogy (precise, not fluffy)
Think of opening a large PDF with 1000 pages:
- Do you load all pages immediately? ❌
- No → you load only when user scrolls to that page ✔️
That “placeholder” before loading = Proxy
Actual page rendering = Real Object
2. Your Doubt (Very Important)
You said:
“display() still takes time — it creates object + calls display — so how is this lazy?”

This is the key misunderstanding.
Let’s break execution timeline
❌ Without Proxy (Naive)
IImage image1 = new RealImage("sample.jpg");

👉 What happens immediately?
- Disk read
- Image decoding
- Memory allocation
Even if you never call display(), cost is already paid.
✔️ With Proxy
IImage image1 = new ImageProxy("sample.jpg");

👉 What happens?
- Only filename stored
- No disk load
- No heavy work
When does cost happen?
image1.display();

Now:
if (realImage == null) {
    realImage = new RealImage(filename); // heavy operation
}
realImage.display();

So what's the actual benefit?
Scenario	Without Proxy	With Proxy
App startup	Slow (loads everything)	Fast
Memory usage	High	Low
Unused objects	Wasteful	Never created
First use latency	Fast	Slight delay


3. Key Insight (This is the answer to your confusion)
Lazy loading does NOT mean zero cost
It means delayed cost

You are shifting:
Cost from → initialization time
           TO
           first usage time

4. Why this matters in real systems
Now think like a system designer.
Example: Instagram Feed
- 100 posts
- Each has images/videos
Without proxy:
- Load all media → slow, huge memory
With proxy:
- Load only visible items
- Others → just placeholders
5. Where your confusion is valid
You are thinking:
“But I still pay cost when calling display()”

Correct. You do.
But the design assumption is:
Not all objects will be used

If ALL objects are always used?
Then proxy is useless.
6. When Virtual Proxy is actually useful
Use it when:
- Object creation is expensive
  - disk IO
  - network call
  - heavy computation
- Object might not be used at all
7. When NOT to use it
Don’t use proxy if:
- Object is cheap to create
- You will definitely use it immediately
- You need ultra-low latency on first call
8. Now think like an engineer (important)
Let me challenge you:
Question:
What happens if:
- 100 users call display() at same time?
- And realImage == null for all?
👉 You may end up creating multiple RealImage objects
This leads to:
- race conditions
- duplicate work
We will fix this in the improved version.
9. Summary (Keep this in mind)
Virtual Proxy is about:
- Not avoiding cost
- Avoiding unnecessary cost

1. Problem Setup (Real-world framing)
Let’s model something close to reality:
You are building a system that displays medical images (MRI/CT scans)

Each image:
- Stored on disk
- Large in size (say 50MB)
- Loading involves:
  - Disk I/O
  - Decoding
  - Memory allocation
2. Naive Design (No Proxy)
We directly create the real object.
Python Implementation
import timeclass IImage:    def display(self):        raise NotImplementedErrorclass RealImage(IImage):    def __init__(self, filename: str):        self.filename = filename        self._load_from_disk()    def _load_from_disk(self):        print(f"[RealImage] Loading image from disk: {self.filename}")        time.sleep(2)  # simulate heavy IO    def display(self):        print(f"[RealImage] Displaying {self.filename}")# ---- Client Code ----if __name__ == "__main__":    print("Creating images...")    image1 = RealImage("scan1.jpg")    image2 = RealImage("scan2.jpg")    image3 = RealImage("scan3.jpg")    print("Images created.\n")    # user only views one image    image1.display()


3. Execution Flow (Step-by-step)
Run mentally:
Creating images...

[RealImage] Loading scan1.jpg  (2 sec)
[RealImage] Loading scan2.jpg  (2 sec)
[RealImage] Loading scan3.jpg  (2 sec)

Images created.

👉 Total delay = 6 seconds
Then:
[RealImage] Displaying scan1.jpg

4. Identify the Problem
Now think like a system designer.
Problem 1: Unnecessary Work
User only viewed:
image1.display()


But we loaded:
- scan2 ❌
- scan3 ❌
👉 Waste of IO + CPU + Memory
Problem 2: Slow Startup
App becomes usable only after all images are loaded
This is dangerous in:
- dashboards
- feeds
- large datasets
Problem 3: Memory Pressure
Each image:
- stays in memory
- even if never used
At scale:
1000 images → crash risk

Problem 4: No Control Over When Cost Happens
Cost is forced at:
image = RealImage(...)


You don’t control timing
5. Where This Breaks at Scale
Let’s push it.
Scenario: Medical dashboard
- 500 patient scans
- Each = 50MB
Naive Behavior
500 × 50MB = 25GB

👉 Impossible to load
Even before memory:
500 × 2 sec = 1000 sec (~16 minutes)

System is unusable.
6. Core Design Flaw
The real issue is:
Object creation is tightly coupled with heavy resource loading

You are doing:
image = RealImage(file)


Which means:
object creation == expensive operation

7. What We Actually Want
We want to separate:
Object reference creation  (cheap)
FROM
Heavy resource loading     (expensive)

8. This leads to Proxy
We want:
image = SomethingLightweight("scan1.jpg")


And only when:
image.display()


👉 THEN load real image


