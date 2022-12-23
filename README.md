# 電影追劇小幫手
## 功能
主要分為兩個功能，第一個功能為搜尋功能，依照選擇的搜尋分類(電影、影集、演員)與輸入的關鍵字來得到搜尋的結果，第二個功能則是熱門清單功能，可以快速得得到當日的熱門電影、影集或是演員，提供給使用者參考。
## 使用要素
### LineBot
使用官方的Line Messaging API實作。
### Flask
使用flask建立後端app。
### TMDb
使用The Movie Database提供的api來獲取即時的電影資料。

下載TMDb api :
```shell
pip install tmdbv3api
```
## FSM Diagram
![](https://i.imgur.com/LnUdC6Q.png)


## 使用教學
- **menu** : 在任何狀態輸入menu(大小寫皆可)即可回到主選單。
- **架構** :
    - 主選單 
    
        輸入`搜尋`進入搜尋模式
        輸入`熱門清單`進入熱門清單模式
        
        ![Minion](https://i.imgur.com/picOaTh.jpg)

        
    - 搜尋模式
        點擊按鈕即可搜尋想要的項目
        
        ![](https://i.imgur.com/WcITSzs.jpg)
        
    - 輸入關鍵字
    
        ![](https://i.imgur.com/ljAB7xj.jpg)
        
    - 顯示搜尋結果

        ![](https://i.imgur.com/rnFVQEY.jpg)
        
    - 點擊想要查看的結果來獲得詳細資訊

        ![](https://i.imgur.com/BYJ7ugy.jpg)
        
    - 影集的搜尋結果

        ![](https://i.imgur.com/scTSSD4.jpg)
        
    - 演員的搜尋結果

        ![](https://i.imgur.com/SLUN6DI.jpg)
        
    - 熱門清單模式(電影)

        ![](https://i.imgur.com/V62lBNo.jpg)
        
    - 熱門清單模式(影集)

        ![](https://i.imgur.com/wqTe8Zb.jpg)
        
    - 熱門清單模式(演員)
        
        ![](https://i.imgur.com/XedUmE0.jpg)
        
    - 隨時輸入menu回到主選單
    
        ![](https://i.imgur.com/IWm7b1m.jpg)






        


        


