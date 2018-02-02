OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
creg c[5];
u3(1.54741470863138,1.53150130858543,-3.37403796121647) q[0];
u3(0.781911948393526,-1.98822144947897,2.73686226858472) q[3];
cx q[3],q[0];
u1(3.28922164743217) q[0];
u3(-1.45457104303452,0.0,0.0) q[3];
cx q[0],q[3];
u3(1.87113651815028,0.0,0.0) q[3];
cx q[3],q[0];
u3(1.78859072096216,-1.15528757897767,3.54028945681494) q[0];
u3(1.45878863499040,-0.919415943536062,4.78257673308859) q[3];
u3(2.64480788628939,-2.34214921826968,1.03501495284446) q[2];
u3(2.65286159302685,-3.75619264586842,-1.35312139606105) q[4];
cx q[4],q[2];
u1(1.49151605370204) q[2];
u3(-0.672683414579476,0.0,0.0) q[4];
cx q[2],q[4];
u3(0.0702998597688194,0.0,0.0) q[4];
cx q[4],q[2];
u3(2.44615534712808,-4.03377015100591,1.09473761466064) q[2];
u3(2.59266608874956,2.39380947074481,3.11649787096613) q[4];
u3(2.74609591384532,0.869049783213149,1.69316909911346) q[1];
u3(1.50098794749798,-2.33082604670270,-2.67721529073882) q[0];
cx q[0],q[1];
u1(2.57364895024244) q[1];
u3(-2.19462095265444,0.0,0.0) q[0];
cx q[1],q[0];
u3(3.02931620930162,0.0,0.0) q[0];
cx q[0],q[1];
u3(2.58802705680260,-2.36771366166962,-0.0157592857908508) q[1];
u3(1.07612186730152,-1.52726195627511,-3.35438755759276) q[0];
u3(1.64389166411013,1.30060689548113,-0.304029927631827) q[4];
u3(0.929300229154258,-0.224522781527408,-3.61241314208412) q[2];
cx q[2],q[4];
u1(1.00604448132869) q[4];
u3(-3.73929527800180,0.0,0.0) q[2];
cx q[4],q[2];
u3(1.71041487314447,0.0,0.0) q[2];
cx q[2],q[4];
u3(1.51507660098324,-4.05893692971606,1.77359304638407) q[4];
u3(1.65513153142619,0.395236838634483,0.698144627446886) q[2];
u3(1.61473048837059,-0.538265520691308,1.96427082494064) q[0];
u3(1.57403014124788,-0.557230131425411,-1.56489918160475) q[3];
cx q[3],q[0];
u1(-1.29896615622248) q[0];
u3(-0.269216273342197,0.0,0.0) q[3];
cx q[0],q[3];
u3(2.69483133194914,0.0,0.0) q[3];
cx q[3],q[0];
u3(2.04619252510806,-2.68796424396085,3.28460413493823) q[0];
u3(1.51874128736768,1.68489138129427,-1.45648647416325) q[3];
u3(2.39005659055632,0.382950392648108,2.64455969983127) q[2];
u3(1.46193061121715,3.12858528258457,2.64349694304938) q[1];
cx q[1],q[2];
u1(1.81729379510946) q[2];
u3(-0.0239295111134885,0.0,0.0) q[1];
cx q[2],q[1];
u3(0.835978064377981,0.0,0.0) q[1];
cx q[1],q[2];
u3(1.59950956658078,-2.16364360998815,1.67902080195540) q[2];
u3(1.99669402971619,-3.95429551220413,-0.959495003015470) q[1];
u3(1.10106768065043,1.21265916086726,-3.77606620070085) q[0];
u3(1.99204451778146,2.25511045932979,-2.50038166977659) q[3];
cx q[3],q[0];
u1(2.10675191359531) q[0];
u3(-2.20683462376896,0.0,0.0) q[3];
cx q[0],q[3];
u3(0.787142547730243,0.0,0.0) q[3];
cx q[3],q[0];
u3(1.33785535033325,-2.62653354693332,-0.105811838243458) q[0];
u3(1.72539982323661,-1.44973796994473,4.38756940637497) q[3];
u3(1.74522690566814,0.460033240682321,1.85837718812925) q[1];
u3(1.73099950507415,-1.20422188474210,-1.60239865511038) q[2];
cx q[2],q[1];
u1(0.437756237367978) q[1];
u3(-1.43821178788192,0.0,0.0) q[2];
cx q[1],q[2];
u3(2.86378330139283,0.0,0.0) q[2];
cx q[2],q[1];
u3(1.43937223837475,-0.848094783768543,0.242849382052781) q[1];
u3(1.16258042833971,-2.06036242156674,-3.16505119407441) q[2];
u3(1.64467484185484,-1.89971412860584,0.916949592273827) q[3];
u3(1.74699137654759,-3.75529909650096,-0.425877024966296) q[4];
cx q[4],q[3];
u1(0.476968381629391) q[3];
u3(-0.805349985365123,0.0,0.0) q[4];
cx q[3],q[4];
u3(1.36235669666024,0.0,0.0) q[4];
cx q[4],q[3];
u3(0.301765617193369,0.633717384609111,0.385771092267203) q[3];
u3(2.77960238815200,-1.66307954735838,0.180939437826076) q[4];
u3(2.37693134147981,-3.15612870296100,3.12461413284101) q[2];
u3(1.45186269343370,3.19311192519123,-1.97700937795069) q[0];
cx q[0],q[2];
u1(0.799424563178180) q[2];
u3(-1.50341750246241,0.0,0.0) q[0];
cx q[2],q[0];
u3(1.85259490750075,0.0,0.0) q[0];
cx q[0],q[2];
u3(1.65333788663255,-1.71150406963161,0.445290116790333) q[2];
u3(0.420740433331540,5.14894508450944,-0.437630024642317) q[0];
barrier q[0],q[1],q[2],q[3],q[4];
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];
measure q[4] -> c[4];