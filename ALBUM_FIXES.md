# Album System Fixes

## Issues Fixed

### 1. ✅ Only Create Albums Based on Top 3 Tags
**Problem:** Albums were created for ALL tags, resulting in too many albums.

**Solution:** 
- Modified `assign_to_albums()` to only use top 3 most relevant tags
- Added `_get_top_tags()` method that prioritizes tags by importance
- Tags are scored using `TAG_PRIORITIES` weights
- High-priority tags: people (100), nature (90), family (95), travel (90), etc.
- Default priority: 50 for unlisted tags

**Implementation:**
```python
# backend/app/services/album_service.py
def _get_top_tags(self, tags: List[str], max_tags: int = 3) -> List[str]:
    # Score and return top 3 tags only
```

---

### 2. ✅ Albums Created Empty (Not Auto-Populated)
**Problem:** Photos were automatically added to albums when uploaded.

**Solution:**
- Changed `assign_to_albums()` to only CREATE albums, not add photos
- Albums are created as empty containers
- Photos must be manually added by user
- Updated function docstring to clarify this behavior

**Key Change:**
```python
# OLD: Added photos automatically
album.media_items.append(media)

# NEW: Just create/ensure album exists
# Photos NOT added - user must add manually
```

---

### 3. ✅ Photo Selection When Creating Albums
**Problem:** No way to add existing photos when creating manual albums.

**Solution:**

#### Backend Changes:
1. **New API Endpoint:** `POST /api/albums/{album_id}/add-photos`
   - Allows adding photos to existing albums
   - Accepts list of media IDs
   - Updates album cover and count

2. **New Request Model:** `AddPhotosRequest`
   ```python
   class AddPhotosRequest(BaseModel):
       media_ids: List[int]
   ```

3. **New Service Method:** `add_media_to_album()`
   - Safely adds photos to albums
   - Checks ownership
   - Prevents duplicates
   - Updates metadata

#### Frontend Changes:
1. **Photo Selection Grid** in create modal
   - Shows all user's photos in a grid
   - Click to select/deselect
   - Visual indicators (blue border + checkmark)
   - Shows selection count

2. **New API Functions:**
   ```javascript
   getAllMedia()          // Fetch all user photos
   addPhotosToAlbum()     // Add photos to album
   ```

3. **Enhanced Create Flow:**
   - Manual tab now shows photo grid
   - Select photos before creating
   - Photos added to album on creation
   - Selection persists until modal closes

---

## Technical Details

### Backend Files Modified:
1. **`app/services/album_service.py`**
   - Modified `assign_to_albums()` - top 3 tags only, no auto-add
   - Added `_get_top_tags()` - smart tag prioritization
   - Added `add_media_to_album()` - manual photo addition

2. **`app/api/routes/albums.py`**
   - Added `AddPhotosRequest` model
   - Added `POST /albums/{id}/add-photos` endpoint
   - Enhanced create album to accept media_ids

### Frontend Files Modified:
1. **`src/utils/api.js`**
   - Added `getAllMedia()`
   - Added `addPhotosToAlbum()`

2. **`src/pages/Albums.jsx`**
   - Added media loading state
   - Added photo selection grid
   - Added selection toggle logic
   - Enhanced modal with photo picker
   - Reset selection on modal close

---

## User Experience

### Creating Albums (AI Search):
1. Click "Create Album"
2. Select "AI Search" tab
3. Enter prompt: "photos with dogs"
4. AI finds and adds matching photos automatically
5. Album created with photos

### Creating Albums (Manual):
1. Click "Create Album"
2. Select "Manual" tab
3. Enter album title
4. **NEW:** Select photos from grid
5. Click "Create Album"
6. Album created with selected photos

### Uploading Photos:
1. Upload photo
2. AI processes and generates top 3 tags
3. **NEW:** Albums created for top 3 tags ONLY
4. **NEW:** Albums are EMPTY (no auto-add)
5. User must manually add photos to albums

---

## Benefits

### 1. Fewer Albums
- Only creates albums for most important 3 tags
- Reduces clutter
- More focused organization

### 2. User Control
- Users decide what goes in albums
- No surprise auto-organization
- Manual curation supported

### 3. Flexible Workflow
- Can create empty albums
- Can create with selected photos
- Can add photos later
- AI search still available

---

## Examples

### Example 1: Photo Upload
**Photo Tags:** ["outdoor", "nature", "tree", "sky", "grass", "landscape", "green"]

**Old Behavior:**
- Created 7 albums
- Photo added to all 7 automatically

**New Behavior:**
- Analyzes tag priorities
- Top 3: "nature" (90), "outdoor" (85), "landscape" (50)
- Creates/ensures 3 albums exist
- Photo NOT added automatically
- User adds to albums manually

### Example 2: Manual Album Creation
**Old Flow:**
1. Create album with title
2. Album is empty
3. No way to add photos

**New Flow:**
1. Create album with title
2. See grid of all photos
3. Select 5 photos
4. Click create
5. Album created with 5 photos

### Example 3: AI Search Album
**Same as before - works perfectly:**
1. Prompt: "sunset beach pictures"
2. AI finds matching photos
3. Album created with all matches
4. Instant, automatic

---

## API Reference

### Add Photos to Album
```bash
POST /api/albums/{album_id}/add-photos
Content-Type: application/json
Authorization: Bearer TOKEN

{
  "media_ids": [1, 2, 3, 4, 5]
}
```

**Response:**
```json
{
  "message": "Added 5 photos to album",
  "total_photos": 5
}
```

### Get All Media
```bash
GET /api/upload/media
Authorization: Bearer TOKEN
```

**Response:**
```json
[
  {
    "id": 1,
    "filename": "photo.jpg",
    "url": "/uploads/photo.jpg",
    ...
  }
]
```

---

## Testing

### Test Photo Upload
1. Upload a photo with multiple tags
2. Check that only 3 albums are created
3. Verify albums are empty
4. Manually add photo to an album

### Test Manual Creation
1. Open Albums page
2. Click "Create Album"
3. Switch to "Manual" tab
4. Verify photo grid appears
5. Select some photos
6. Create album
7. Verify photos are in album

### Test AI Search
1. Upload photos with "dog" tags
2. Create album: "all photos with dogs"
3. Verify matches are found and added

---

## Migration Notes

### Existing Albums
- No migration needed
- Old albums remain unchanged
- New behavior applies to new uploads only

### Database
- No schema changes
- Uses existing tables and relationships
- Backward compatible

---

## Summary

All three issues have been resolved:

✅ **Top 3 Tags Only** - Smart prioritization prevents album spam
✅ **Empty Albums** - Albums created but not auto-populated  
✅ **Photo Selection** - Full UI for selecting photos when creating albums

The system now provides:
- Better organization (fewer, more focused albums)
- User control (manual photo management)
- Flexibility (AI search OR manual selection)
- Professional workflow (create with photos OR add later)
