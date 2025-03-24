# 一、系統性雜訊注入設計

## 1. 數據集選擇參考
- 醫療領域：優先使用原始論文中的12個 Microarray 數據集（如Leukemia），這些數據集已包含部分雜訊。
- 擴展數據集：新增3個公開數據集進行驗證：
  1. 高維小樣本：Gistette (5000特徵, 6000樣本)、Madelon (500特徵, 200樣本)
  2. 類別不平衡：Credit Fraud (284k樣本, 0.17%異常)
  3. 混合特徵類型：UCI Adult (數值+類別型)
- 合成數據集：使用`sklearn.datasets.make_classification`生成可控雜訊結構的數據。

## 2. 雜訊類型
| 雜訊類別             | 表示式                             | 意義                     | 強度分類參考                   |
|----------------------|------------------------------------|--------------------------|--------------------------------|
| Gaussian noise       | $X_{noisy} = X + N(0, \sigma^2)$  | 儀器測量誤差          | $\sigma \in \{0.1, 0.3, 0.5\}$ |
| Missing data         | $X_{ij} = NaN$ (機率p)             | 數據遺失              | $p \in \{0.1, 0.3, 0.5\}$   |
| Redundant feature    | 插入隨機特徵                   | 無關特徵          | 冗余比例如 $\{0.2, 0.5\}$    |
| Adversarial perturbation | FGSM攻擊 $X + \epsilon * \text{sign}(V)$ | 惡意竄改數據              | $\epsilon \in \{0.1, 0.3, 0.5\}$ |

---
參考資料:
- /Gistette https://archive.ics.uci.edu/dataset/170/gisette
- https://github.com/juansucre/madelon
- https://paperswithcode.com/dataset/kaggle-credit-card-fraud-dataset
- https://archive.ics.uci.edu/dataset/2/adult
