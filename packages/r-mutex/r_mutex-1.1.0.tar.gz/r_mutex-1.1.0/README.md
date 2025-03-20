### **Overview**
A distributed asynchronous lock built on top of the Redis PubSub, Get and Set methods. This takes inspiration from the asyncio Lock whereby futures are used instead of the polling done by the multiprocessing Lock.

It's free to be built upon locally for your needs. Optionally you can do `pip install r-mutex`

### **Requirements**
- Redis
- Python 3.12.6
If you don't have Redis but have docker you can simply run this command.
`docker run --name <name> -d -p 6379:6379`

If you want to see the messages being sent back and forth in real-time you can do
```
docker exec -it <name> redis-cli
SUBSCRIBE <key>.live or <key>.broadcast
```

### **Contact**
https://www.linkedin.com/in/jadore-t-49379a295/
https://twitter.com/jtzenz