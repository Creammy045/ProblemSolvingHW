import streamlit as st

# -------------------- Song Class --------------------
class Song:
    def __init__(self, title, artist, file):
        self.title = title
        self.artist = artist
        self.file = file
        self.next_song = None

    def __str__(self):
        return f"{self.title} by {self.artist}"

# -------------------- MusicPlaylist (Linked List) --------------------
class MusicPlaylist:
    def __init__(self):
        self.head = None
        self.current_song = None
        self.length = 0

    def add_song(self, title, artist, file):
        new_song = Song(title, artist, file)
        if self.head is None:
            self.head = new_song
            self.current_song = new_song
        else:
            current = self.head
            while current.next_song:
                current = current.next_song
            current.next_song = new_song
        self.length += 1
        st.success(f"Added: {new_song}")

    def display_playlist(self):
        songs = []
        current = self.head
        i = 1
        while current:
            marker = "▶️ " if current == self.current_song else ""
            songs.append(f"{marker}{i}. {current.title} - {current.artist}")
            current = current.next_song
            i += 1
        return songs

    def next_song(self):
        if self.current_song and self.current_song.next_song:
            self.current_song = self.current_song.next_song

    def prev_song(self):
        if self.head is None or self.current_song == self.head:
            return
        temp = self.head
        while temp.next_song != self.current_song:
            temp = temp.next_song
        self.current_song = temp

    def delete_song(self, title):
        if self.head is None:
            return
        if self.head.title == title:
            self.head = self.head.next_song
            self.current_song = self.head
            self.length -= 1
            return
        prev, curr = None, self.head
        while curr and curr.title != title:
            prev, curr = curr, curr.next_song
        if curr:
            prev.next_song = curr.next_song
            if self.current_song == curr:
                self.current_song = prev
            self.length -= 1

# -------------------- UI --------------------
st.set_page_config(page_title="Music Playlist", layout="centered")
st.title("🎵 Music Playlist Player (Linked List)")

if "playlist" not in st.session_state:
    st.session_state.playlist = MusicPlaylist()

# ---------- Sidebar ----------
st.sidebar.header("➕ Add Song")
title = st.sidebar.text_input("Song Title")
artist = st.sidebar.text_input("Artist")
file = st.sidebar.file_uploader("Upload MP3 / WAV", type=["mp3", "wav"])

if st.sidebar.button("Add to Playlist"):
    if title and artist and file:
        st.session_state.playlist.add_song(title, artist, file)
    else:
        st.sidebar.warning("กรอกชื่อเพลง ศิลปิน และอัปโหลดไฟล์")

st.sidebar.header("🗑 Delete Song")
del_title = st.sidebar.text_input("Song Title to Delete")
if st.sidebar.button("Delete"):
    st.session_state.playlist.delete_song(del_title)

# ---------- Playlist Display ----------
st.subheader("📜 Playlist")
for s in st.session_state.playlist.display_playlist():
    st.write(s)

st.markdown("---")

# ---------- Centered Audio Player ----------
st.markdown(
    """
    <style>
    audio {
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

player = st.empty()
if st.session_state.playlist.current_song:
    player.audio(st.session_state.playlist.current_song.file)

# ---------- Controls ----------
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("⏮ Prev"):
        st.session_state.playlist.prev_song()
        if st.session_state.playlist.current_song:
            player.audio(st.session_state.playlist.current_song.file)

with c2:
    if st.button("▶ Play"):
        if st.session_state.playlist.current_song:
            player.audio(st.session_state.playlist.current_song.file)

with c3:
    if st.button("⏭ Next"):
        st.session_state.playlist.next_song()
        if st.session_state.playlist.current_song:
            player.audio(st.session_state.playlist.current_song.file)

st.markdown("---")
st.write(f"🎶 Total songs: {st.session_state.playlist.length}")
