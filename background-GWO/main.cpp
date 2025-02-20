#include <iostream>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <limits>

using namespace std;

const int DIM = 2; //dimension
const int WOLF_COUNT = 10; 
const int MAX_ITER = 100000; //intration
const double LB = 0;  // lower bound
const double UB = 3; // upper bouud

// 個別狼隻對於假想最佳解的距離(網路上也說叫做目標適應度)
double fitnessFunction(const vector<double>& position) {
    double fitness = 0;

    // Arg type 1 
    if (position[0]<2){
        fitness = numeric_limits<double>::max();
    }else{
        fitness = abs(pow(position[1],2) - position[0]);
    }
    //fitness = 
    
    //Arg ype 2 
    /* for (size_t i = 0; i < DIM; i++) {  //不知道為甚麼這樣最佳解不是 1.07
        fitness += abs(cos(position[i]));
    }  */
    return fitness;
}


double randDouble(double min, double max) {
    return min + (max - min) * ((double)rand() / RAND_MAX);
}

// 初始化狼群的位置，只使用一次
void initializeWolves(vector<vector<double>>& wolves, vector<double>& fitness) {
    for (size_t i = 0; i < WOLF_COUNT; i++) {
        for (size_t j = 0; j < DIM; j++) {
            wolves[i][j] = randDouble(LB, UB);
        }
        fitness[i] = fitnessFunction(wolves[i]);
    }
}

// 更新狼群位置，一開始的三隻領頭狼更新，之後的狼群在三隻領頭狼附近隨機移動
void updateWolves(vector<vector<double>>& wolves, vector<double>& fitness, vector<double>& alpha, vector<double>& beta, vector<double>& gamma, int& iter) {
    // 找出 alpha、beta、gamma
    double alphaFit = numeric_limits<double>::max();
    double betaFit = numeric_limits<double>::max();
    double gammaFit = numeric_limits<double>::max();

    for (size_t i = 0; i < WOLF_COUNT; i++) { // 找出 alpha、beta、gamma(目標是應函數前三最小者)
        if (fitness[i] < alphaFit) {
            gamma = beta;
            gammaFit = betaFit;
            beta = alpha;
            betaFit = alphaFit;
            alpha = wolves[i];
            alphaFit = fitness[i];
        } else if (fitness[i] < betaFit) {
            gamma = beta;
            gammaFit = betaFit;
            beta = wolves[i];
            betaFit = fitness[i];
        } else if (fitness[i] < gammaFit) {
            gamma = wolves[i];
            gammaFit = fitness[i];
        }
    }
    
    // 更新每隻狼的位置，每隻狼會更新[維度]次
    for (size_t i = 0; i < WOLF_COUNT; i++) { 
        auto current_wolve = wolves[i];
        for (size_t j = 0; j < DIM; j++) {
            double a = 2 - 2 * ((MAX_ITER-iter)/MAX_ITER);  //隨時間變化的參數 a

            double A1 = a * (2 * ((double)rand() / RAND_MAX) - 1);  //距離隨機參數
            double A2 = a * (2 * ((double)rand() / RAND_MAX) - 1);
            double A3 = a * (2 * ((double)rand() / RAND_MAX) - 1);
            
            double C1 = 2 * ((double)rand() / RAND_MAX); //領頭狼位置隨機權重參數
            double C2 = 2 * ((double)rand() / RAND_MAX);
            double C3 = 2 * ((double)rand() / RAND_MAX);
            
            double D_alpha = fabs(C1 * alpha[j] - current_wolve[j]); //隨機狼與兩頭狼距離
            double D_beta = fabs(C2 * beta[j] - current_wolve[j]);
            double D_gamma = fabs(C3 * gamma[j] - current_wolve[j]);
            
            double X1 = alpha[j] - A1 * D_alpha; //目標位置
            double X2 = beta[j] - A2 * D_beta;
            double X3 = gamma[j] - A3 * D_gamma;
            
            wolves[i][j] = (X1 + X2 + X3) / 3; //平均三個目標位置
            
            // 限制範圍
            if (wolves[i][j] < LB) wolves[i][j] = LB;
            if (wolves[i][j] > UB) wolves[i][j] = UB;
        }
        fitness[i] = fitnessFunction(wolves[i]); // 更新目標適應度
    }
}

int main() {
    srand(static_cast<unsigned int> (time(0)));
    
    vector<vector<double>> wolves(WOLF_COUNT, vector<double>(DIM)); // 狼群  [狼隻數量][空間維度]
    vector<double> fitness(WOLF_COUNT);  // 目標適應函數集合
    
    // 初始狼群
    initializeWolves(wolves, fitness);
    int iter = 0;
    
    // Alpha、Beta、Gamma 狼
    vector<double> alpha(DIM), beta(DIM), gamma(DIM);
    updateWolves(wolves, fitness, alpha, beta, gamma, iter);
    
    for (iter = 0; iter < MAX_ITER; iter++) {
        updateWolves(wolves, fitness, alpha, beta, gamma, iter);
        //cout << "Iteration " << iter + 1 << ": Best fitness = " << fitnessFunction(alpha) << endl;
    }
    
    cout << "Best solution found: ";
    for (double val : alpha) cout << val << " ";
    cout << "\nBest fitness: " << fitnessFunction(alpha) << endl;
    
    return 0;
}
