### Bank Simulator
這是一個銀行模擬器，但現在有個問題是它的存錢(deposit)、取錢(withdraw)、轉帳(transfer)等功能是缺失的，請你幫我們找到正確的函式，並且找到對的地方進行呼叫，讓deposit、withdraw、transfer等功能正常運行!

- **目標Objective:**  
  Practice using Git and GitHub by forking a repository, creating a new file, and making a commit with a proper commit message.

- **Instructions & Steps:**  
  1. **Fork this repository & 切換到studentVersion branch:**  
     - Fork下來這樣你才能自由使用 :D
     - 請記得fork的時候把這一個checkbox取消
     <img width="707" height="108" alt="image" src="https://github.com/user-attachments/assets/ba2208c6-8ad1-48fc-bd13-1c84e82d1a60" />
     

     - studentVersion branch 是給你們練習的版本，當然燒機太久想看答案，答案就在main branch裡面，自行運用。 :D
  
  2. **編輯dockerfile與compose.yml**  
     - 讓此app能以網站的形式跑起來
     - 預設開啟的網址為 localhost:5000/
       
     - 還未編輯dockerfile與compose.yml前想先看網站模樣，記得先用以下指令安裝所需套件:
       ```
       pip install -r requirement.txt
       ```
     - 接著用以下指令: 
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
     若什麼都沒做的話將看到 3 fail ....
     <img width="1065" height="82" alt="image" src="https://github.com/user-attachments/assets/a1d6d411-4c6a-4a84-a9f6-60b25f6b335e" />

     而你的工作就是把它處裡到全部success!
     
    
- **Submission Requirements:**  
  Push your commits to GitHub ensuring the commit message follows the guidelines.
