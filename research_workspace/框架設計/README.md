# 一、系統性雜訊注入設計

## 1. 數據集選擇參考
- 醫療領域：優先使用原始論文中的12個 Microarray 數據集（如Leukemia），這些數據集已包含部分雜訊。
- 擴展數據集：新增3個公開數據集進行驗證：
  1. 高維小樣本：Gistette (5000特徵, 6000樣本)、Madelon (500特徵, 200樣本)
  2. 類別不平衡：Credit Fraud (284k樣本, 0.17%異常)
  3. 混合特徵類型：UCI Adult (數值+類別型)
- 合成數據集：使用`sklearn.datasets.make_classification`生成可控雜訊結構的數據。
### 數據集來源:
- Gistette [手寫數字辨識](https://archive.ics.uci.edu/dataset/170/gisette)
- Madelon [高維度/非線性資料](https://github.com/juansucre/madelon)
- Credit Fraud [信用卡交易/詐騙數](https://paperswithcode.com/dataset/kaggle-credit-card-fraud-dataset)
- UCI Adult [預測年收入](https://archive.ics.uci.edu/dataset/2/adult)


## 2. 雜訊類型
| 雜訊類別             | 表達式                             | 意義                     | 強度分類參考                   |
|----------------------|------------------------------------|--------------------------|--------------------------------|
| Gaussian noise       | $X_{noisy} = X + N(0, \sigma^2)$  | 儀器測量誤差          | $\sigma \in \{0.1, 0.3, 0.5\}$ |
| Missing data         | $X_{ij} = NaN$ (機率p)             | 數據遺失              | $p \in \{0.1, 0.3, 0.5\}$   |
| Redundant feature    | 插入隨機特徵                   | 無關特徵          | 冗餘比例如 $\{0.2, 0.5\}$    |
| Adversarial perturbation | FGSM攻擊 $X + \epsilon * \text{sign}(V)$ | 惡意竄改數據              | $\epsilon \in \{0.1, 0.3, 0.5\}$ |

---
# 二、基於雜訊特徵的EDGWO改進方法

## 先前實作

## 預計優化方向
### 1.動態多目標適應機制

- **問題**：單目標優化（準確率+特徵數）在雜訊下易 overfitting  
- **解決方法**：引入 Pareto 前沿概念，定義雙適應度函數：

$$
\begin{cases} 
f_1 = \lambda \cdot \text{ErrorRate} + (1 - \lambda) \cdot |S| \ & (\text{特徵數}) \
f_2 = \text{FeatureStability} & (\text{特徵選擇穩定性}) 
\end{cases}
$$ 

``` 註： 簡單來說，這個方法就是在兩個衝突的要素之間做取捨(特徵數量 vs. 準確率) ```

穩定性透過Bootstrap採樣計算[Jaccard](https://blog.csdn.net/qq_34333481/article/details/84024513)相似度。

``` 註： A向量 -> 隨機抽樣的特徵 subset;B向量 -> 選取的特徵 subset ```

---
參考資料:
[《Robust Feature Selection via Nonconvex Sparse Learning》 (JMLR 2023)](https://dl.acm.org/doi/10.5555/3454287.3455398)
