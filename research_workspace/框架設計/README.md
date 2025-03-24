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

## 先前優化EDGWO實作
1. ##### 指數衰減 `(a = 2 * np.exp(-t / self.MAX_ITER))`

    - 作用：控制搜索範圍，讓早期探索空間較大，後期收斂較快。
    - 優勢：避免收斂過慢，提高全局(global)搜索能力。

2. ##### 自適應突變 `(if (self.PreAlpha_score - self.alpha_score) < eps)`

    - 作用：當最佳適應值變化極小時，對 10% 的個體進行突變，擾動隨時間遞減。
    - 優勢：避免陷入局部最佳解，提供額外的探索能力。

3. ##### 多樣性維護 `(if diversity < 0.01 * np.mean(self.ub - self.lb):)`

    - 作用：當群體多樣性過低時，隨機重置 20% 的狼，確保狼群不會過度集中。
    - 優勢：防止搜索範圍過度收縮，提高演算法的適應性。

並且進行了一些實驗，與 EDGWO 比較收斂性，結果如下:

<div>
    <div style="display: flex; flex-wrap: wrap;">
        <div style="flex: 1; padding: 5px;">
            <img src="./exp_result_1/_EDGWO vs. REIN_EDGWO/2021_F3_10D.png" alt="P_CEC2021-F3" style="width: 70%;">
        </div>
        <div style="flex: 1; padding: 5px;">
            <img src="./exp_result_1/_EDGWO vs. REIN_EDGWO/2021_F4_20D.png" alt="R_CEC2021-F4" style="width: 70%;">
        </div>
       <div style="flex: 1; padding: 5px;">
            <img src="./exp_result_1/_EDGWO vs. REIN_EDGWO/2021_F7_20D.png" alt="R_CEC2021-F7" style="width: 70%;">
        </div>
    </div>
</div>


## 預計優化方向
### 1.動態多目標適應機制

- **問題**：單目標優化（準確率+特徵數）在雜訊下易 overfitting  
- **解決方法**：引入 Pareto 前沿概念，定義雙適應度函數(再取加權平均)：

$$
\begin{cases} 
f_1 = \lambda \cdot \text{ErrorRate} + (1 - \lambda) \cdot |S| & (\text{特徵數}) \\ 
f_2 = \text{FeatureStability} & (\text{特徵選擇穩定性}) 
\end{cases}
$$

``` 註： 簡單來說，這個方法就是在兩個衝突的要素之間做取捨(特徵數量 vs. 準確率) ```

穩定性透過Bootstrap採樣計算[Jaccard](https://blog.csdn.net/qq_34333481/article/details/84024513)相似度。

``` 註： A向量 -> 隨機抽樣的特徵 subset;B向量 -> 選取的特徵 subset ```

---
參考資料:
[《Robust Feature Selection via Nonconvex Sparse Learning》 (JMLR 2023)](https://dl.acm.org/doi/10.5555/3454287.3455398)
