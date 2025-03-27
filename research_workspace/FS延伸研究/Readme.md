# FS_GWO 研究說明

## 研究目標

- 研究GWO類優化器在特徵選擇領域上的做法，主要分為三個部分：
  1. 適應特徵選擇問題的方法；
  2. 在特徵選擇上遇到雜訊時的反應；
  3. 結合前兩者，探討GWO類優化器在特徵選擇問題上的應用。

## 目前研究說明

- BGWO for FS

- FS for face recognition(classcification)
  - 使用了經典電腦視覺方法來搭配GWO處裡視覺辨識。
  - 先背知識點太多，暫緩執行。

- GWO&CSA with Unconstrain FS

- GWO&GOA for text FS

  1. 研究目標
    - 結合GWO和GOA，以提升FS的效果。
    - 改善文本分類的準確率，並降低不必要的特徵數量，以提高演算法的效率。

  2. 使用的演算法
    - GWO：模擬灰狼的狩獵行為來進行全域搜尋，具有良好的全域探索能力。
    - GOA：模擬草食動物尋找食物的行為，適合局部搜尋和細節優化。
    - GWO-GOA 混合：利用GWO的全域搜尋能力和GOA的局部搜尋能力，讓特徵選取更精確。

  3. 結論
    - 相較於單獨使用GWO或GOA，GWO-GOA 混合方法能選取較少但更具代表性的特徵。
    - 未來可以進一步結合其他演算法，如PSO或GA。

- hybrid Gradient descent GWO for FS
  - 增加gradient decent(梯度下降方法)來加入局部收斂，加快收斂factor的同時，可以確立局部收斂的穩定性。
  - HowTo: 透過目標函數的「準確度上升率」來給予激勵機制或懲罰機制。

## 留言板

- 我其實很好奇為什麼我們一開始在在FS時效果可以這麼好。GWO FS在一開始的定義上其實只是找出最佳參數，但我們的結果出現了多次 acc = 100% 的情況。 kai 2025/3/22

## 研究進度

- 2025/3/22: 開始研究hybrid Gradient descent GWO for FS
- 2025/3/23: 開始研究FS for face recognition(classcification)
- 2025/3/27: 大致閱讀GWO&GOA for text FS
