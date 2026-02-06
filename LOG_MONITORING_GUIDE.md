# AllCanLearn-v3 Log Monitoring Guide

## ✅ Setup Complete!

Your v3 now has comprehensive logging enabled. This will help us diagnose issues when changes don't appear.

## 🎯 What's Logged

1. **Server startup/shutdown**
2. **All HTTP requests** (GET, POST, etc.)
3. **Response times**
4. **Errors and exceptions**
5. **Application events**

## 📊 View Logs from Mac

### Quick Check
```bash
cd "/Users/vikki/Desktop/AI Roundtable/AI-Roundtable"
./check-v3-logs.sh
```

### Detailed View
```bash
# Live streaming (see requests in real-time)
ssh vikki@192.168.1.138 '~/AllCanLearn-v3/view-logs.sh live'

# Recent logs
ssh vikki@192.168.1.138 '~/AllCanLearn-v3/view-logs.sh recent'

# Errors only
ssh vikki@192.168.1.138 '~/AllCanLearn-v3/view-logs.sh errors'

# HTTP requests
ssh vikki@192.168.1.138 '~/AllCanLearn-v3/view-logs.sh requests'
```

## 🔍 Diagnostic Workflow

When you make changes and they don't work:

### Step 1: Check if server restarted
```bash
./check-v3-logs.sh
```
Look for: `Started server process` with a new PID

### Step 2: Check for errors
```bash
ssh vikki@192.168.1.138 '~/AllCanLearn-v3/view-logs.sh errors'
```

### Step 3: Verify files synced
```bash
ssh vikki@192.168.1.138 'ls -lt ~/AllCanLearn-v3/app/static/index.html | head -1'
```
Check the timestamp - should be recent

### Step 4: Test specific page
```bash
curl -I http://192.168.1.138:8002/
```
Should return `200 OK`

### Step 5: Watch live logs while testing
```bash
# Terminal 1: Watch logs
ssh vikki@192.168.1.138 '~/AllCanLearn-v3/view-logs.sh live'

# Terminal 2: Make request
curl http://192.168.1.138:8002/
```

## 🚨 Common Issues & Solutions

### Issue: Changes not appearing
**Check:**
1. Did sync complete? Look for "✅ Sync complete!"
2. Did server restart? Look for new PID in logs
3. Browser cache? Hard refresh: `Cmd+Shift+R`

**Solution:**
```bash
# Force sync and restart
cd "/Users/vikki/Desktop/AI Roundtable/AI-Roundtable"
./sync-v3-to-ubuntu.sh
```

### Issue: Server not responding
**Check:**
```bash
ssh vikki@192.168.1.138 'ps aux | grep uvicorn.*8002'
```

**Solution:**
```bash
ssh vikki@192.168.1.138 '~/AllCanLearn-v3/start-server-with-logging.sh'
```

### Issue: 404 errors for static files
**Check logs for:**
```
GET /static/assets/image.jpg - 404
```

**Solution:**
Verify file exists on Ubuntu:
```bash
ssh vikki@192.168.1.138 'ls ~/AllCanLearn-v3/app/static/assets/image.jpg'
```

## 📝 Log File Locations

**Ubuntu Server:**
- Main log: `~/AllCanLearn-v3/server.log`
- App logs: `~/AllCanLearn-v3/logs/app.log` (if enabled)

## 🔄 Workflow Going Forward

1. **Make changes on Mac** in `AllCanLearn-v3/`
2. **Sync to Ubuntu**: `./sync-v3-to-ubuntu.sh`
3. **Check logs**: `./check-v3-logs.sh`
4. **Test in browser**: http://192.168.1.138:8002
5. **If issues**: View live logs while testing

## 💡 Pro Tips

- Keep a terminal with live logs open while developing
- Check logs immediately after sync
- Browser cache can hide updates - always hard refresh
- Logs show exact file paths requested - helpful for 404s

## 🎯 Next Steps

Now when you say "changes aren't working", we can:
1. Check logs to see if files were requested
2. See exact error messages
3. Verify server received the updates
4. Diagnose caching vs actual bugs

**Test it now:**
1. Run `./check-v3-logs.sh`
2. Open http://192.168.1.138:8002 in browser
3. Check logs again - you'll see the HTTP requests!
