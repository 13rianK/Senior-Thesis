%% Sensor Data Plots
close all
clear all

data1 = csvread('gesture1.csv');

data1(:,1) = data1(:,1)*0.0049;
data1(:,2) = data1(:,2)*0.0049;
data1(:,3) = data1(:,3)*0.0049;
data1(:,4) = data1(:,4)*0.0049;
data1(:,5) = data1(:,5)*0.0049;

time = linspace(0,2);

figure
hold on;

plot(time, data1(:,1),'LineWidth',2);
plot(time, data1(:,2),'LineWidth',2);
plot(time, data1(:,3),'LineWidth',2);
plot(time, data1(:,4),'LineWidth',2);
plot(time, data1(:,5),'LineWidth',2);
title('Flex Sensor Response of "Open Hand to Closed Fist" Gesture');
xlabel('Time (s)');
ylabel('Volts (V)');
legend('Thumb','Index','Middle','Ring','Pinky');

% plot(time, data1(:,6),'LineWidth',2);
% plot(time, data1(:,7),'LineWidth',2);
% plot(time, data1(:,8),'LineWidth',2);
% xlabel('Time (s)');
% ylabel('Degrees');
% legend('Roll','Pitch','Yaw')
% title('IMU Response of "Open Hand to Pointing" Gesture');

%% kNN Results

clear all
close all

figure
set(gca,'fontsize',18);
% data = csvread('knn3output.csv');
data = csvread('PCB2_kNN2Out.csv');
k = linspace(1, 499, 500);
plot(k,data, 'LineWidth',2)
xlabel('k','fontsize',18);
ylabel('% Correctly Recognized','fontsize',18)
title('kNN Results for Varying Values of k','fontsize',18)

figure
data = csvread('knn3output_sqrt.csv');
k = linspace(1, 499, 250);
plot(k,data, 'LineWidth',2)
xlabel('k','fontsize',18);
ylabel('% Correctly Recognized','fontsize',18)
title('kNN Results for Varying Values of k (distance calculated with square root)','fontsize',18)

%% Output from kNN with Binary flex values

figure
% data = csvread('knn4output.csv');
data = csvread('PCB2_kNN4OUt.csv');
k = linspace(1, 499, 250);
plot(k,data, 'LineWidth',2)
xlabel('k','fontsize',24);
ylabel('% Correctly Recognized','fontsize',24)
title('kNN Results on for Varying Values of k (Binary Values)','fontsize',24)

%% Flex Sensor Angle Characterization Graphs
clear all
close all

a180 = csvread('angle180.csv');
a170 = csvread('angle170.csv');
a160 = csvread('angle160.csv');
a150 = csvread('angle150.csv');
a140 = csvread('angle140.csv');
a130 = csvread('angle130.csv');
a120 = csvread('angle120.csv');
a110 = csvread('angle110.csv');
a100 = csvread('angle100.csv');
a90 = csvread('angle90.csv');

figure(8)
hold on
X = linspace(180,90,10);

index = linspace(1,2,10);
middle = linspace(1,2,10);
ring = linspace(1,2,10);
pinky = linspace(1,2,10);
error = linspace(1,2,10);

% Really ugly code to turn everything into averages and std deviations
index(10) = mean(a90(:,2));
err(10) = std(a90(:,2));
index(9) = mean(a100(:,2));
err(9) = std(a100(:,2));
index(8) = mean(a110(:,2));
err(8) = std(a110(:,2));
index(7) = mean(a120(:,2));
err(7) = std(a120(:,2));
index(6) = mean(a130(:,2));
err(6) = std(a130(:,2));
index(5) = mean(a140(:,2));
err(5) = std(a140(:,2));
index(4) = mean(a150(:,2));
err(4) = std(a150(:,2));
index(3) = mean(a160(:,2));
err(3) = std(a160(:,2));
index(2) = mean(a170(:,2));
err(2) = std(a170(:,2));
index(1) = mean(a180(:,2));
err(1) = std(a180(:,2));
e1 = errorbar(X, index*0.00322, err*0.00322, 'linewidth', 2);
e1.Color = 'red';

middle(10) = mean(a90(:,3));
err(10) = std(a90(:,3));
middle(9) = mean(a100(:,3));
err(9) = std(a100(:,3));
middle(8) = mean(a110(:,3));
err(8) = std(a110(:,3));
middle(7) = mean(a120(:,3));
err(7) = std(a120(:,3));
middle(6) = mean(a130(:,3));
err(6) = std(a130(:,3));
middle(5) = mean(a140(:,3));
err(5) = std(a140(:,3));
middle(4) = mean(a150(:,3));
err(4) = std(a150(:,3));
middle(3) = mean(a160(:,3));
err(3) = std(a160(:,3));
middle(2) = mean(a170(:,3));
err(2) = std(a170(:,3));
middle(1) = mean(a180(:,3));
err(1) = std(a180(:,3));
e2 = errorbar(X, middle*0.00322, err*0.00322, 'linewidth', 2);
e2.Color = 'blue';

ring(10) = mean(a90(:,4));
err(10) = std(a90(:,4));
ring(9) = mean(a100(:,4));
err(9) = std(a100(:,4));
ring(8) = mean(a110(:,4));
err(8) = std(a110(:,4));
ring(7) = mean(a120(:,4));
err(7) = std(a120(:,4));
ring(6) = mean(a130(:,4));
err(6) = std(a130(:,4));
ring(5) = mean(a140(:,4));
err(5) = std(a140(:,4));
ring(4) = mean(a150(:,4));
err(4) = std(a150(:,4));
ring(3) = mean(a160(:,4));
err(3) = std(a160(:,4));
ring(2) = mean(a170(:,4));
err(2) = std(a170(:,4));
ring(1) = mean(a180(:,4));
err(1) = std(a180(:,4));
e2 = errorbar(X, ring*0.00322, err*0.00322, 'linewidth', 2);
e2.Color = 'green';

pinky(10) = mean(a90(:,5));
err(10) = std(a90(:,5));
pinky(9) = mean(a100(:,5));
err(9) = std(a100(:,5));
pinky(8) = mean(a110(:,5));
err(8) = std(a110(:,5));
pinky(7) = mean(a120(:,5));
err(7) = std(a120(:,5));
pinky(6) = mean(a130(:,5));
err(6) = std(a130(:,5));
pinky(5) = mean(a140(:,5));
err(5) = std(a140(:,5));
pinky(4) = mean(a150(:,5));
err(4) = std(a150(:,5));
pinky(3) = mean(a160(:,5));
err(3) = std(a160(:,5));
pinky(2) = mean(a170(:,5));
err(2) = std(a170(:,5));
pinky(1) = mean(a180(:,5));
err(1) = std(a180(:,5));
e2 = errorbar(X, pinky*0.00322, err*0.00322, 'linewidth', 2);
e2.Color = 'magenta';

legend('Index','Middle','Ring','Pinky');
xlabel('Angle of Fingers (Degrees)','fontsize',18);
ylabel('Voltage Measurement (V)','fontsize',18);
% axis([80 190 1.5 5]);
title('Flex Sensor Angle Characterization','fontsize',18);

%% Random Forest
clear all
close all

% data = csvread('randomForestResults.csv');
data = csvread('PCB2_RFOut.csv');
X = linspace(10,250,24);

figure (7)
e = errorbar(X, 100*data(:,1), 100*data(:,2), 'linewidth', 2);
e.Marker = '*';
xlabel('Number of Estimators');
ylabel('Percentage Correct (%)')
axis([5 255 93 100])
title('Random Forest Results for Various Estimators')

%% Real Time Accuracy

data = csvread('realtime_results.csv');
a = unique(data(:,1));
counts = [a,histc(data(:,1),a)]
correct = out(2,2)/(out(2,2)+out(1,2))

%% Real Time Accuracy with Bluetooth

data = csvread('realtimeBluetooth_results.csv');
a = unique(data(:,1));
counts = [a,histc(data(:,1),a)]
correct = counts(2,2)/(counts(2,2)+counts(1,2))