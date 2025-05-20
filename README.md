📍**這個小工具可以用來模擬特定投資期間、特定標的，使用定期定額的投資報酬率**

(目前是非常陽春的初版, 還有一些細節在改, 歡迎提供我UI/UX相關的建議呦)

📖 操作流程:

1. 打開瀏覽器輸入 http://35.229.191.8:30081/docs 
   (網址有點醜, 因為懶得註冊DNS哈哈)

2. 進來之後會看到這個swagger UI的畫面

![Screenshot from 2025-05-20 10-53-14](https://github.com/user-attachments/assets/d6b035cd-4198-4187-a110-774e00fc5fbd)
 
3. 點一下**GET/simulate**那個藍色框框, 然後點右側的**Try it out**按鈕, 就可以輸入資訊啦!
   
   說明一下這些欄位:
   
      * symbol: 輸入Yahoo Finance上的股票代號, 台股或美股皆可
        例如台積電輸入 2330.TW、NVDIA輸入NDVA...等等
      * start_date: 投資期間起始日
      * end_date: 投資期間結束日
      * single_dates: 每月定期定額的日期 (若想比較在不同日期扣款的投報率, 可多選) 
        按Add integer item可以新增更多日期, 按方框右邊的"-"可以刪除日期
        總共分為兩種策略, 一種是把每月的投資金額分散在不同的兩日(每月扣款兩次, 雙日策略); 一種是每月僅扣款一次(單日策略)
        計算之結果會按照單日策略以及雙日策略的投報率結果由高到低排序
      * monthly_investment: 每月定期定額投資的金額
  
   💡範例:
   
    ![Screenshot from 2025-05-20 11-15-12](https://github.com/user-attachments/assets/ef4d356b-b200-4b02-8bc8-b97a59d2c036)

    查詢在**2025-01-01~2025-05-01**期間, 定期定額投資APPLE(股票代號**AAPL**), 計算在每個月的**1.8.15.22.28**這幾個日子扣款、使用不同策略的報酬率
    (單日策略: 這五個日子選一天扣10000; 雙日策略: C5取2選兩天, 一天扣5000)
        
 4. 都輸入完成後按 **Execute**, 計算的結果會出現在下方Response的區塊
    
    以剛剛的範例來說, 結果會長這樣:
    
    ![Screenshot from 2025-05-20 11-25-45](https://github.com/user-attachments/assets/2fed1277-f7ee-4a26-b6a4-1e122dd97a49)

    在這個**Response body**的框框裡面往下滾動視窗就可以看到完整結果啦! 大功告成!

    但因為我是免費仔用Google雲端的免費額度, 所以網路有點爛🤡 有時候可能會出現這個error:
    
    ![Screenshot from 2025-05-20 11-13-50](https://github.com/user-attachments/assets/7b2e537b-cf57-486c-a136-6ddb330a154d)

    不要怕再多按幾次 Execute就會成功了! 除非內容有錯誤(股票代號或日期格式錯誤)才會報錯, 像是這樣:
    
    ![Screenshot from 2025-05-20 11-28-33](https://github.com/user-attachments/assets/e95d65ab-83b7-417f-a452-23eedd4d9cd6)

    (Error handling的部份我還沒去做, 所以錯誤訊息也長得蠻醜的🤣)


    
