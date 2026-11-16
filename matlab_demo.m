% 2D Geometric Transformations - MATLAB demonstration
% Matches the report's triangle A(1,1), B(3,1), C(2,3).

clc; clear; close all;

% Homogeneous vertices stored as columns; repeat first point to close shape.
tri = [1 3 2 1;
       1 1 3 1;
       1 1 1 1];

T = @(tx,ty) [1 0 tx; 0 1 ty; 0 0 1];
S = @(sx,sy) [sx 0 0; 0 sy 0; 0 0 1];
R = @(d) [cosd(d) -sind(d) 0;
          sind(d)  cosd(d) 0;
          0        0       1];
Shx = @(k) [1 k 0; 0 1 0; 0 0 1];
Shy = @(k) [1 0 0; k 1 0; 0 0 1];
Rx = [1 0 0; 0 -1 0; 0 0 1];
Ry = [-1 0 0; 0 1 0; 0 0 1];
Ro = [-1 0 0; 0 -1 0; 0 0 1];

% Rotate by 90 degrees, then scale by 2.
M = S(2,2) * R(90);
out = M * tri;

disp('Original triangle:');
disp(tri(1:2,1:3));
disp('Rotated 90 degrees, then scaled by 2:');
disp(out(1:2,1:3));

figure;
plot(tri(1,:), tri(2,:), 'b-o', 'LineWidth', 2);
hold on;
plot(out(1,:), out(2,:), 'r-o', 'LineWidth', 2);
axis equal; grid on;
legend('Original', 'Transformed');
title('2D Geometric Transformation');

% Rotation about centroid (2, 5/3).
cx = 2; cy = 5/3;
Mcentroid = T(cx,cy) * R(90) * T(-cx,-cy);
outCentroid = Mcentroid * tri;

figure;
plot(tri(1,:), tri(2,:), 'b-o', 'LineWidth', 2);
hold on;
plot(outCentroid(1,:), outCentroid(2,:), 'r-o', 'LineWidth', 2);
axis equal; grid on;
legend('Original', 'Rotated about centroid');
title('Rotation About an Arbitrary Point');
