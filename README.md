# song-guess
Guess the song!  

這是一個猜歌遊戲  
題庫來源來自於 KKBOX playlist  
只要下關鍵字搜尋playlist後，選擇喜歡的歌單後即可出題來玩！  
目前提供2種玩法：  
  
1. 聽一段前奏或歌曲後，進行答題：https://song-guess.fly.dev  
2. 由機器人念出歌詞後，進行答題：https://song-guess.fly.dev/lyric  

並可顯示解答，包含：歌名、歌手、專輯名、專輯發行日期、專輯封面等  


技術實作：  
歌曲及題目來源皆使用 KKBOX api 進行串接  
歌詞部分與 MusixMatch api 進行串接

如想clone回本機執行，則須申請KKBOX & MusixMatch 相關授權並記錄於.env  

