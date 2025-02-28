# 移動優化灰狼演算法 Elite-driven-Grey-Wolf-Optimization
> 程式碼內仍有大量的註解程式區塊，其為為後續更新做準備或具備除錯用途

## package requirements
- `opfunu` 
- `numpy`
- `matplotlib`
- `tqdm`
- `scipy`
- `scikit-learn`
<!-- 
## 或您也可以直接執行編譯文件main.exe
- 透過 `nuitka` 將 `main.py` 編譯成 `main.exe`，並且將其放置於 `dist` 資料夾中，您可以直接執行 `main.exe` 來進行優化測試。 -->

## 使用方法: 
本專案實作了 **Elite-driven Grey Wolf Optimization (EDGWO)**，並比較多種論文中提及的優化演算法的性能，適用於不同的數據集與適應函數 **(CEC Dataset與Gene Dataset)**。使用者可以透過輸入選擇特定的函數來進行優化，並透過**平行計算**執行多種演算法，最終輸出優化結果與可視化圖表。
1. ### 執行 `main.py` 進行優化測試
   主程式會執行不同的優化演算法，並針對所選**fitness function**進行多次iterations，運行後可透過輸入來選擇測試參數。
2. ### 設定優化演算法 `ConfigClass.py`
   透過調整 `ConfigClass.py` 選擇可用演算法的class，也可以在完成演算法後，直接演算法控制器加入CongigClass中，快速進行接入主程式。
3. ### Fitness function/Dataset `DataSet.py`
   該檔案負責管理 CEC 和GENE數據集的Fitness function

## 程式碼說明:
1. `main.py`: 主程式，此程式包含觀察者主架構組件，可以操控所有變量，並且可以呼叫EDGWO和GWO等演算法。
2. `DataSet.py`: 適應函數(Fitness function)，此程式包含所有的適應函數，可以透過此程式來呼叫適應函數。
3. `ConfigClass`: 設定檔，此程式包含所有的設定檔，可以透過此程式來設定部分的變量。
3. `演算法.py`: 各式演算法，包含演算法的主要架構，包含初始化、適應函數、更新、選擇以該演算法與主程式的交互介面。
    > NOTE: `REINEDGWO.py`為優化版的EDGWO演算法
4. `LiveDemo.py`: 用於展示演算法的實時運行狀況，可以透過此程式來觀察演算法的運行狀況。(然而，只支援2維資料且僅能單獨運行)


## 觀察者架構
1. _MainControl_: 主要架構，包含所有的變量，並且可以購過Config中的演算法註冊列表來個別呼叫 _Algos_ Control。
2. _Algos_ Control: 演算法控制架構，包含確保固定的演算法變數傳入，並且可以呼叫該演算法並執行及處裡回傳結果，可以稱其為演算法的API。
3. _Algos_: 個別為11種演算法架構，內有演算法的基礎邏輯，由 _Algos_ Control 呼叫並執行，並且回傳結果。


# 實驗數據
## 1. 連續函數實驗結果與論文對照
### CEC2021 In 10-Dimension
| 論文數據 | 實驗結果 |
|----------|---------|
| 📌 F3 ![論文 F3](./convergence_curve/CEC2021/2021_F3_10D_paper.jpg) | ✅ F3 ![我的 F3](./convergence_curve/CEC2021/2021_F3_10D.png) |
| 📌 F6 ![論文 F6](./convergence_curve/CEC2021/2021_F6_10D_paper.jpg) | ✅ F6 ![我的 F6](./convergence_curve/CEC2021/2021_F6_10D.png) |
| 📌 F8 ![論文 F8](./convergence_curve/CEC2021/2021_F8_10D_paper.jpg) | ✅ F8 ![我的 F8](./convergence_curve/CEC2021/2021_F8_10D.png) |
| 📌 F10 ![論文 F10](./convergence_curve/CEC2021/2021_F10_10D_paper.jpg) | ✅ F10 ![我的 F10](./convergence_curve/CEC2021/2021_F10_10D.png) |

### CEC2021 In 20-Dimension
| 論文數據 | 實驗結果 |
|:--------:|:--------:|
| 📌 F4 ![論文 F4](./convergence_curve/CEC2021/2021_F4_20D_paper.jpg) | ✅ F4 ![我的 F4](./convergence_curve/CEC2021/2021_F4_20D.png) |
| 📌 F7 ![論文 F7](./convergence_curve/CEC2021/2021_F7_20D_paper.jpg) | ✅ F7 ![我的 F7](./convergence_curve/CEC2021/2021_F7_20D.png) |
| 📌 F8 ![論文 F8](./convergence_curve/CEC2021/2021_F8_20D_paper.jpg) | ✅ F8 ![我的 F8](./convergence_curve/CEC2021/2021_F8_20D.png) |
| 📌 F9 ![論文 F9](./convergence_curve/CEC2021/2021_F9_20D_paper.jpg) | ✅ F9 ![我的 F9](./convergence_curve/CEC2021/2021_F9_20D.png) |

### CEC2022 In 10-Dimension
| 論文數據 | 實驗結果 |
|:--------:|:--------:|
| 📌 F2 ![論文 F2](./convergence_curve/CEC2022/2022_F2_10D_paper.jpg) | ✅ F2 ![我的 F2](./convergence_curve/CEC2022/2022_F2_10D.png) |
| 📌 F6 ![論文 F6](./convergence_curve/CEC2022/2022_F6_10D_paper.jpg) | ✅ F6 ![我的 F6](./convergence_curve/CEC2022/2022_F6_10D.png) |
| 📌 F8 ![論文 F8](./convergence_curve/CEC2022/2022_F8_10D_paper.jpg) | ✅ F8 ![我的 F8](./convergence_curve/CEC2022/2022_F8_10D.png) |
| 📌 F12 ![論文 F12](./convergence_curve/CEC2022/2022_F12_10D_paper.jpg) | ✅ F12 ![我的 F12](./convergence_curve/CEC2022/2022_F12_10D.png) |

### CEC2022 In 20-Dimension
| 論文數據 | 實驗結果 |
|:--------:|:--------:|
| 📌 F7 ![論文 F7](./convergence_curve/CEC2022/2022_F7_20D_paper.jpg) | ✅ F7 ![我的 F7](./convergence_curve/CEC2022/2022_F7_20D.png) |
| 📌 F9 ![論文 F9](./convergence_curve/CEC2022/2022_F9_20D_paper.jpg) | ✅ F9 ![我的 F9](./convergence_curve/CEC2022/2022_F9_20D.png) |
| 📌 F10 ![論文 F10](./convergence_curve/CEC2022/2022_F10_20D_paper.jpg) | ✅ F10 ![我的 F10](./convergence_curve/CEC2022/2022_F10_20D.png) |
| 📌 F11 ![論文 F11](./convergence_curve/CEC2022/2022_F11_20D_paper.jpg) | ✅ F11 ![我的 F11](./convergence_curve/CEC2022/2022_F11_20D.png) |




### 2. 自優化REIN-EDGWO vs EDGWO 實驗對照 :
我們有稍微針對EDGWO進行了一些改進，並且將其命名為REIN-EDGWO，主要優化方式如下:
1. #### 指數衰減 `(a = 2 * np.exp(-t / self.MAX_ITER))`
- 作用：控制搜索範圍，讓早期探索空間較大，後期收斂較快。
- 優勢：避免收斂過慢，提高全局(global)搜索能力。
2. #### 自適應突變 `(if (self.PreAlpha_score - self.alpha_score) < eps)`
- 作用：當最佳適應值變化極小時，對 10% 的個體進行突變，擾動隨時間遞減。
- 優勢：避免陷入局部最佳解，提供額外的探索能力。
3. #### 多樣性維護 `(if diversity < 0.01 * np.mean(self.ub - self.lb):)`
- 作用：當群體多樣性過低時，隨機重置 20% 的狼，確保狼群不會過度集中。
- 優勢：防止搜索範圍過度收縮，提高演算法的適應性。

並且進行了一些實驗，與EDGWO比較收斂性，結果如下:
<div>
    <div style="display: flex; flex-wrap: wrap;">
        <div style="flex: 1; padding: 5px;">
            <img src="_EDGWO vs. REIN_EDGWO\2021_F3_10D.png" alt="P_CEC2021-F3" style="width: 70%;">
        </div>
        <div style="flex: 1; padding: 5px;">
            <img src="_EDGWO vs. REIN_EDGWO\2021_F4_20D.png" alt="R_CEC2021-F4" style="width: 70%;">
        </div>
       <div style="flex: 1; padding: 5px;">
            <img src="_EDGWO vs. REIN_EDGWO\2021_F7_20D.png" alt="R_CEC2021-F7" style="width: 70%;">
        </div>
    </div>
</div>

### 3. 離散資料實驗結果(11種optimizer):
| ALLML 7129D | Leukemia_1 5327D |
|:--------:|:--------:|
| ![論文 F4](./_EXP_PIC/ALLAML-30(2).png) | ![我的 F4](_EXP_PIC\Leukemin-30N.png) |

論文中使用二值方式來代表分類資料集的"啟用"與否(也就是該特徵將被乘上0或1表示是否被納入計算)
 而我們的做法是使浮點數來代表該維度的加權數字，讓期能有在指定曲見內有更多種組合方式(但相對的，也更難找到Optimal)。

兩者相同的是，都是透過KNN來進行分類，並且計算準確率當作適應函數值。


## 總結
_本專案：_
- **實作了 EDGWO，並針對 EDGWO 進行強化，透過實驗數據顯示REIN-EDGWO 在多數函數上優於 EDGWO**
- **比較了多種演算法的適應值與收斂速度**
- **以Dataset驗證演算法之效能**
- **提供收斂曲線圖與數離散資料實驗結果，量化演算法優化效果，使結果更具說服力。**
- **嘗試以訓練加權參數的方式訓練具有類別的離散資料。 詳細該資料帶回分類器(KNN)結果，計算準確率當作適應函數值。**
- **提供了一個可擴展的架構，可以輕鬆添加新的演算法，並且可以進行多種演算法的比較。**


