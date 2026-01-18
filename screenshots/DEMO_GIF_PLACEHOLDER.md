# Demo GIF Placeholder

This file should be replaced with your actual demo GIF showing the LLM Banking Agent in action.

## Recommended Content for Demo GIF

Your demo GIF should showcase:

1. **Application Overview**
   - User interface
   - User switching feature
   - Clean, professional look

2. **Basic Functionality**
   - User logging in
   - Requesting transactions
   - Viewing transaction history

3. **Security Features** (Optional)
   - Attempting an attack
   - Security alert being triggered
   - Comparison of vulnerable vs secure version

## Technical Specifications

- **Format**: GIF or MP4 (converted to GIF)
- **Duration**: 10-30 seconds
- **Size**: < 5MB (for GitHub)
- **Resolution**: 1280x720 or similar
- **Frame Rate**: 10-15 fps for smooth playback

## How to Create

### Option 1: Screen Recording to GIF
```bash
# macOS - Use QuickTime + ffmpeg
# 1. Record with QuickTime (Cmd+Shift+5)
# 2. Convert to GIF
ffmpeg -i recording.mov -vf "fps=10,scale=1280:-1:flags=lanczos" -c:v gif demo.gif
```

### Option 2: Use LICEcap (Free)
- Download: https://www.cockos.com/licecap/
- Record directly to GIF
- Easy to use, cross-platform

### Option 3: Use Gifski (High Quality)
```bash
# Install gifski
brew install gifski

# Convert video to GIF
gifski -o demo.gif --fps 10 --quality 90 recording.mp4
```

## Optimization

To reduce file size:
```bash
# Using gifsicle
gifsicle -O3 --lossy=80 -o demo-optimized.gif demo.gif
```

---

**Current Status**: Placeholder - Replace with actual demo GIF

**Target Location**: `screenshots/demo.gif`
