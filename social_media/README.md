# Social media & NBA sales analysis
## 目的:探討社群(以Reddit為例)與球隊銷售之間的關係
### 實作1:利用Reddit上某些場次比賽的upward number(類似讚數)、comment number及該比賽觀眾數當training data，產生一個model，未來便可利用此model和upward number、comment number來預測觀眾人數
### 實作2:使用情緒分析套件分析網友回文內容，藉以得知某個時期大眾對該球隊的反應


## 流程
### 實作1:
- (1)爬NBA網站獲得賽程和觀眾人數資料
- (2)爬Reddit獲得比賽相關文章，在Reddit上各個球隊都有自己的板，板上有網友在賽前提供的比賽描述文章(但並非每場比賽都有文章)
- (3)文字處理將(1)和(2)資料merge在一起
- (4)linear regression生成model
