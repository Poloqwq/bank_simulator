### Bank Simulator
這是一個銀行模擬器，但現在有個問題是它的存錢(deposit)、取錢(withdraw)、轉帳(transfer)等功能是缺失的，請你幫我們找到正確的函式，並且找到對的地方進行呼叫，讓deposit、withdraw、transfer等功能正常運行!

- **目標Objective:**  
  Practice using Git and GitHub by forking a repository, creating a new file, and making a commit with a proper commit message.

- **Instructions & Steps:**  
  1. **Fork this repository & 切換到studentVersion branch:**  
     - Fork下來這樣你才能自由使用 :D
     - studentVersion branch 是給你們練習的版本，當然燒機太久想看答案，答案就在main branch裡面，自行運用。 :D
  2. **編輯dockerfile與compose.yml**  
     - 讓此app能以網站的形式跑起來
     - 預設開啟的網址為 localhost:5000/
     - 還未編輯dockerfile與compose.yml前，可以用以下指令: 
       ```
       python backend/routers/app.py
       ```
       去開啟網站，預設網址也是 localhost:5000/
  3. **查找可用的工具函式**  
     - 東西都在 backend 裡面了，去尋找吧!
     - 閱讀 models 裡面的程式邏輯，對作業有幫助以外，你對網頁前後端也會有理解喔! uwu
  4. **實作**  
     - 找到正確的函式，並且找到對的地方進行呼叫
  5. **測試**  
     - 進行測試指令:
     ```
     pytest .\tests\test_app_routes.py
     ```
     若什麼都沒做的話將看到 4 fail ....
     而你的工作就是把它處裡到全部success!
     
    
- **Submission Requirements:**  
  Push your commits to GitHub ensuring the commit message follows the guidelines.
