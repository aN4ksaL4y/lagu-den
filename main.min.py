_c='disoriented'
_b='free-spirited'
_a='serene'
_Z='mysterious'
_Y='frustrated'
_X='heartbroken'
_W='celebratory'
_V='optimistic'
_U='curious'
_T='rebellious'
_S='grateful'
_R='excited'
_Q='adventurous'
_P='hopeful'
_O='anxious'
_N='playful'
_M='motivated'
_L='reflective'
_K='inspired'
_J='nostalgic'
_I='confident'
_H='melancholic'
_G='romantic'
_F='focused'
_E='energetic'
_D='lonely'
_C='artists'
_B='name'
_A='items'
import spotipy,sqlite3,json,time
from spotipy.oauth2 import SpotifyClientCredentials
import os
SPOTIPY_CLIENT_ID='2a552506817c47cb8c21b80d88c9d406'
SPOTIPY_CLIENT_SECRET='09b1459c7a784014923af0de39a138d0'
auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET)
sp=spotipy.Spotify(auth_manager=auth_manager)
def get_recently_played(sp):A=sp.current_user_recently_played(limit=50);return A[_A]
def get_mood_input():
	B=['happy','sad',_E,'calm',_F,_G,'angry',_H,_I,_J,'chill',_K,_L,_D,_M,_N,_O,_P,_Q,'tired',_R,_S,_T,_U,_V,_W,_X,_Y,_Z,_a,_b,'silly',_c];print('What mood are you in? Choose from the following:');C=0
	for D in B:C+=1;print(C,D)
	A=input('Enter your mood: ').lower()
	try:
		if A in B:return A
		if A.isdigit():E=int(A);A=B[E-1];return A
	except Exception as F:print('Please choose the right number or type the mood.',F)
def get_playlist_for_mood(mood):
	A='pop';B={'happy':A,'sad':'acoustic',_E:'electronic','calm':'ambient',_F:'classical',_G:'r&b','angry':'metal',_H:'indie',_I:'hip-hop',_J:'retro','chill':'lo-fi',_K:'indie folk',_L:'jazz',_D:'blues',_M:'rock',_N:'funk',_O:'trip-hop',_P:'gospel',_Q:'world','tired':'downtempo',_R:'dance',_D:'country',_S:'soul',_T:'punk',_U:'experimental',_V:'synthwave',_W:'latin',_X:'folk',_Y:'industrial',_Z:'psychedelic',_a:'new age',_b:'reggae','silly':'electro swing',_c:'drone'};C=B.get(mood,A)
	try:D=sp.search(q=f"genre:{C}",type='playlist',limit=20);return D['playlists'][_A]
	except Exception as E:return'Try decreased limit'
def get_playlist_tracks(playlist_link):
	C=playlist_link.split('/')[-1].split('?')[0];D=sp.playlist_tracks(C);B=[]
	for E in D[_A]:
		try:
			A=E['track']
			if A:F=A[_B];G=', '.join(A[_B]for A in A[_C]);H={'artist':G,'title':F};B.append(H)
		except Exception as I:print(I)
	return B
def get_song_genre(song_name,artist_name=None):
	G='tracks';C=artist_name;B=song_name;D=B
	if C:D+=f" artist:{C}"
	E=sp.search(q=D,type='track',limit=1)
	if E[G][_A]:
		A=E[G][_A][0];H=A[_C][0]['id'];I=sp.artist(H);F=I.get('genres',[])
		if F:print(f"Genres for {A[_B]} by {A[_C][0][_B]}: {", ".join(F)}")
		else:print(f"No genres found for {A[_C][0][_B]}")
	else:print(f"No results found for song: {B}")
if __name__=='__main__':print('ok')