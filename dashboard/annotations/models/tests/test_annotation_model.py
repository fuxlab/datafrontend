from django.test import TestCase

from projects.models import Project

from datasets.models import Dataset
from images.models import Image
from categories.models import Category
from annotations.models import Annotation

import numpy as np
class TestAnnotationModels(TestCase):


    def setUp(self):
        self.project = Project.objects.create(name='Testproject 1')
        self.dataset = Dataset.objects.create(name='test', project=self.project)
        self.image = Image.objects.create(url='123456', dataset=self.dataset)
        self.category = Category.objects.create(name='category1', project=self.project)


    def test_get_coords_from_segmentation(self):
        x_min, x_max, y_min, y_max = Annotation.get_coords_from_segmentation([10,10,20,10,20,20,10,20])
        self.assertEqual(x_min, 10)
        self.assertEqual(x_max, 20)
        self.assertEqual(y_min, 10)
        self.assertEqual(y_max, 20)

    
    def test_get_coords_from_segmentation_real(self):
        data = [
            [481.08, 2.98, 509.26, 38.74, 563.43, 56.07, 599.19, 84.24, 615.44, 125.42, 640.0, 157.92, 640.0, 110.25, 637.11, 2.98, 486.5, 1.9],
            [96.43, 88.58, 268.71, 5.15, 114.85, 0.81, 149.53, 49.57, 100.77, 75.58, 89.93, 87.49],
            [539.59, 460.23, 633.86, 402.8, 633.86, 474.31, 535.26, 467.81],
            [539.59, 460.23, 633.86, 402.8, 633.86, 474.31, 535.26, 467.81],
            [539.59, 460.23, 633.86, 402.8, 633.86, 474.31, 535.26, 467.81],
        ]
        x_min, x_max, y_min, y_max = Annotation.get_coords_from_segmentation(data)
        
        self.assertEqual(x_min, 89.93)
        self.assertEqual(x_max, 640.0)
        self.assertEqual(y_min, 0.81)
        self.assertEqual(y_max, 474.31)

    
    def test_get_coords_from_segmentation_another_real(self):
        '''
        some big data caused trouble, so we should take care
        '''
        data = [
            [[
                425.09, 315.19, 422.69, 307.98, 411.88, 302.58, 406.47, 301.37, 406.09, 306.68, 417.45, 311.23, 423.41, 315.2, 412.05, 313.78, 406.37, 307.25, 402.68, 303.27,
                401.54, 299.01, 397.85, 300.15, 392.74, 297.31, 388.47, 297.59, 387.91, 299.3, 383.65, 295.04, 381.09, 297.88, 387.34, 303.84, 393.3, 302.71, 399.27, 304.69,
                404.1, 306.4, 410.35, 313.22, 410.35, 314.07, 402.68, 313.22, 387.34, 310.66, 382.79, 303.84, 378.53, 299.3, 377.4, 296.17, 373.14, 295.6, 372.28, 299.01,
                378.82, 301.28, 386.2, 310.66, 381.09, 310.66, 376.54, 307.53, 368.02, 301.0, 370.23, 299.11, 371.04, 296.15, 366.87, 293.19, 364.05, 293.06, 363.25, 296.55,
                367.28, 299.51, 368.62, 302.73, 380.58, 310.93, 371.58, 305.69, 366.07, 301.12, 360.69, 296.28, 362.04, 293.19, 360.56, 291.18, 354.24, 291.18, 353.03, 288.36,
                349.54, 288.09, 346.72, 288.89, 347.79, 291.04, 351.02, 293.6, 348.73, 297.36, 350.75, 298.43, 355.99, 296.82, 360.42, 297.23, 368.22, 303.67, 377.36, 309.72,
                379.24, 310.93, 374.53, 309.32, 371.17, 309.99, 366.47, 308.11, 364.59, 307.17, 360.02, 308.65, 354.65, 305.56, 349.0, 300.32, 341.21, 293.19, 343.23, 292.39,
                342.02, 289.03, 338.93, 287.69, 335.7, 288.36, 333.15, 288.22, 335.84, 290.91, 341.61, 294.94, 349.41, 301.66, 354.11, 306.23, 348.47, 305.15, 346.72, 304.62,
                339.87, 298.17, 330.46, 289.97, 326.03, 286.21, 331.4, 287.55, 333.55, 287.55, 332.07, 284.46, 328.98, 283.39, 326.16, 283.92, 324.95, 284.86, 323.07, 282.98,
                323.2, 280.16, 319.71, 277.88, 316.22, 278.28, 315.81, 281.24, 311.65, 281.37, 307.89, 284.46, 308.96, 286.48, 310.44, 287.01, 314.61, 285.54, 321.19, 285.54,
                325.35, 288.09, 333.55, 294.67, 343.9, 304.08, 338.25, 303.94, 335.3, 301.26, 331.13, 298.97, 324.01, 290.91, 318.77, 285.94, 316.76, 286.34, 328.98, 298.3,
                330.19, 299.91, 326.97, 299.38, 325.76, 298.43, 324.41, 299.91, 320.38, 296.55, 315.81, 291.72, 310.98, 287.28, 309.1, 286.88, 308.02, 285.0, 303.05, 281.24,
                299.15, 277.34, 296.33, 274.11, 294.32, 272.9, 290.96, 273.44, 289.08, 275.86, 289.88, 278.28, 294.05, 276.94, 297.81, 279.22, 301.17, 281.64, 308.96, 288.22,
                314.61, 293.46, 317.43, 295.88, 311.65, 295.88, 311.11, 294.27, 309.63, 294.27, 305.87, 291.58, 300.63, 286.07, 292.7, 278.41, 292.57, 277.88, 290.69, 278.28,
                296.87, 284.06, 304.39, 291.58, 301.57, 291.31, 297.81, 291.18, 296.47, 291.85, 295.79, 289.43, 294.05, 289.57, 289.75, 286.48, 286.52, 284.33, 279.8, 278.55,
                273.22, 273.17, 268.25, 268.34, 265.02, 265.25, 262.74, 263.1, 261.66, 261.75, 259.38, 263.36, 261.66, 266.59, 265.02, 269.95, 269.19, 271.96, 277.92, 279.76,
                286.12, 285.8, 282.36, 285.8, 280.07, 285.8, 276.85, 282.71, 266.5, 273.31, 258.04, 266.32, 253.87, 261.89, 251.72, 259.87, 247.56, 258.39, 243.93, 259.87,
                242.72, 261.89, 245.41, 264.04, 248.9, 263.9, 252.93, 262.83, 258.04, 267.53, 266.9, 275.32, 276.31, 283.52, 274.29, 283.92, 271.74, 281.77, 267.44, 279.76,
                262.34, 278.68, 261.93, 277.34, 257.5, 274.92, 251.86, 270.62, 243.66, 263.36, 234.79, 255.97, 235.19, 254.23, 232.64, 251.54, 230.49, 251.41, 228.34, 249.12,
                224.71, 248.99, 224.85, 253.29, 228.34, 255.17, 231.3, 256.38, 236.81, 259.74, 252.39, 272.77, 254.54, 274.92, 249.57, 274.38, 244.73, 273.31, 241.64, 274.52,
                239.09, 271.7, 232.77, 265.78, 223.5, 257.72, 217.86, 251.81, 218.26, 249.12, 215.84, 247.78, 214.1, 247.91, 211.68, 245.9, 207.78, 246.03, 206.57, 243.88,
                205.5, 243.34, 200.26, 248.05, 201.06, 248.18, 204.56, 246.97, 206.57, 246.97, 206.57, 248.05, 201.87, 250.6, 202.41, 251.81, 205.77, 252.21, 209.53, 251.14,
                212.75, 251.67, 214.64, 253.96, 216.52, 253.29, 224.44, 260.54, 240.3, 275.32, 238.02, 274.92, 231.43, 269.81, 231.7, 269.14, 226.59, 267.4, 223.64, 266.72,
                222.29, 267.4, 218.67, 266.99, 214.64, 268.87, 209.26, 264.3, 206.84, 262.42, 204.69, 261.48, 204.56, 259.6, 201.87, 259.06, 199.72, 260.54, 189.51, 253.56,
                185.61, 250.06, 182.92, 246.43, 179.43, 242.54, 177.01, 243.61, 176.21, 247.51, 179.43, 250.06, 175.53, 251.0, 172.44, 251.14, 166.93, 250.47, 160.08, 251.41,
                158.33, 251.41, 152.29, 246.97, 143.96, 243.21, 145.03, 241.06, 147.32, 238.37, 149.47, 237.57, 149.87, 237.57, 148.12, 236.22, 146.38, 236.22, 144.09, 237.3,
                142.34, 238.51, 141.27, 241.46, 139.79, 240.79, 139.93, 237.97, 142.34, 233.8, 143.55, 222.38, 145.03, 218.62, 147.72, 215.26, 147.05, 213.65, 145.17, 214.19,
                142.08, 217.95, 140.6, 221.71, 139.52, 221.84, 139.39, 216.87, 138.18, 216.6, 137.24, 219.56, 136.43, 224.53, 134.82, 227.89, 133.61, 233.13, 131.46, 238.37,
                130.92, 240.12, 126.89, 235.15, 122.73, 231.92, 118.56, 231.38, 113.99, 231.38, 110.63, 233.8, 109.69, 235.42, 109.42, 238.91, 107.14, 241.46, 104.72, 241.73,
                100.69, 240.92, 99.48, 239.45, 95.18, 234.34, 95.32, 230.85, 98.81, 220.9, 101.23, 212.04, 99.62, 209.62, 97.87, 208.54, 95.05, 208.27, 92.76, 210.15, 91.69,
                211.77, 87.52, 219.02, 86.45, 219.83, 80.0, 209.75, 79.25, 203.9, 76.34, 201.71, 70.87, 196.24, 66.4, 191.36, 64.5, 190.67, 62.6, 190.32, 59.67, 193.08, 58.81,
                195.67, 60.36, 200.15, 66.4, 213.08, 64.38, 228.74, 62.98, 227.34, 57.83, 210.49, 52.8, 201.78, 47.65, 192.77, 44.43, 190.19, 39.93, 188.91, 36.71, 191.48, 35.42,
                197.27, 39.61, 204.35, 41.86, 206.93, 38.32, 207.89, 37.35, 208.54, 36.07, 212.4, 38.32, 219.48, 44.76, 232.67, 38.32, 227.84, 34.78, 227.84, 39.93, 230.74, 44.43,
                236.53, 41.22, 235.89, 38.0, 235.25, 36.07, 237.82, 40.25, 237.82, 43.79, 242.97, 40.57, 243.61, 36.39, 243.61, 33.49, 242.65, 32.53, 240.07, 30.92, 241.04, 34.78,
                245.87, 37.03, 246.19, 32.85, 248.76, 29.31, 257.13, 30.27, 264.53, 32.13, 256.04, 33.85, 251.39, 39.03, 248.8, 42.82, 251.04, 46.62, 248.46, 49.03, 250.53, 46.44,
                255.53, 44.55, 261.22, 45.24, 270.87, 48.68, 278.12, 52.65, 281.91, 50.89, 270.44, 50.89, 255.47, 59.78, 242.84, 70.07, 241.9, 79.43, 243.31, 80.83, 248.45, 78.49,
                252.2, 82.49, 268.71, 77.98, 281.26, 76.05, 285.44, 75.41, 293.49, 72.83, 297.03, 70.26, 305.07, 66.15, 322.3, 63.0, 329.66, 67.77, 327.66, 73.79, 327.66, 82.56,
                334.93, 85.82, 337.43, 88.33, 336.93, 93.59, 336.93, 103.62, 331.67, 108.14, 342.95, 109.14, 353.73, 116.09, 374.43, 109.54, 375.36, 98.31, 369.28, 90.82, 364.13,
                89.89, 365.07, 96.44, 370.68, 110.94, 378.17, 118.43, 376.77, 119.75, 389.41, 126.57, 381.17, 134.23, 375.78, 137.08, 372.65, 133.1, 359.3, 129.41, 343.96, 121.45,
                332.6, 123.44, 327.2, 131.39, 345.38, 136.79, 363.28, 136.51, 350.49, 138.78, 357.31, 141.9, 350.49, 137.36, 338.28, 124.58, 318.11, 123.44, 316.69, 126.0, 316.12,
                136.51, 326.92, 146.17, 341.69, 148.15, 337.71, 140.2, 326.63, 129.97, 314.42, 127.42, 312.43, 134.8, 303.62, 138.5, 297.66, 137.95, 293.55, 137.29, 290.01, 136.4,
                289.12, 137.07, 283.15, 136.18, 280.71, 141.05, 282.93, 147.91, 283.81, 153.67, 284.03, 158.09, 281.82, 166.51, 288.68, 174.92, 291.12, 185.76, 291.56, 191.29, 289.12,
                199.04, 296.65, 208.78, 298.64, 215.2, 298.2, 219.18, 296.87, 225.6, 302.62, 232.68, 304.4, 240.21, 304.4, 243.08, 302.85, 249.95, 309.04, 254.59, 310.37, 261.68,
                310.59, 263.45, 309.49, 275.57, 317.1, 288.37, 325.77, 292.09, 327.84, 293.43, 329.74, 296.53, 328.85, 297.86, 330.63, 296.09, 334.83, 296.97, 336.6, 300.29, 335.05,
                301.18, 341.91, 302.95, 345.23, 306.27, 343.68, 306.49, 337.27, 309.81, 341.91, 310.25, 348.33, 316.89, 346.34, 320.65, 349.66, 320.88, 352.76, 318.88, 354.97, 321.54,
                359.62, 326.41, 356.52, 327.52, 349.44, 323.97, 344.35, 320.43, 341.91, 316.23, 342.13, 313.57, 337.71, 311.8, 334.61, 306.49, 331.73, 301.62, 325.09, 298.52, 320.67,
                295.2, 318.23, 288.56, 318.89, 279.49, 314.91, 289.23, 318.01, 296.97, 317.79, 298.74, 319.56, 303.17, 322.44, 306.27, 323.54, 322.43, 341.03, 338.9, 359.21, 340.04,
                362.9, 341.74, 366.03, 345.31, 366.79, 347.79, 373.4, 348.24, 365.64, 345.67, 360.81, 341.81, 358.56, 337.95, 357.92, 326.68, 343.76, 312.85, 328.31, 308.72, 324.18,
                313.37, 324.18, 315.58, 327.06, 321.78, 328.38, 338.03, 346.3, 352.67, 360.2, 354.57, 361.93, 355.43, 365.03, 357.68, 366.41, 357.68, 370.2, 360.61, 376.58, 360.09,
                371.41, 360.43, 368.82, 362.5, 366.58, 361.12, 361.75, 357.85, 360.03, 354.23, 359.51, 350.6, 356.23, 343.36, 348.99, 335.43, 341.4, 323.87, 327.95, 327.84, 327.26,
                329.74, 329.33, 331.98, 329.68, 344.05, 342.27, 354.23, 353.3, 361.99, 361.24, 365.61, 366.93, 365.95, 371.07, 368.37, 373.31, 366.99, 378.48, 364.57, 380.55, 370.21,
                377.58, 371.09, 371.82, 372.64, 370.27, 372.2, 367.17, 369.99, 364.96, 368.0, 363.85, 366.23, 363.85, 362.68, 358.54, 353.61, 349.25, 341.21, 335.97, 335.68, 331.1,
                341.66, 330.21, 357.81, 347.25, 375.3, 366.29, 376.19, 368.94, 379.06, 370.49, 376.41, 373.15, 375.74, 375.14, 379.28, 377.13, 377.96, 382.0, 381.5, 373.81, 382.16,
                368.5, 380.83, 364.74, 376.85, 363.85, 366.89, 353.67, 348.08, 334.2, 348.3, 332.42, 352.5, 331.54, 355.38, 334.42, 369.1, 349.02, 385.04, 366.51, 387.25, 370.05,
                388.8, 373.15, 387.03, 377.58, 391.01, 372.49, 392.12, 369.17, 389.91, 365.62, 386.81, 364.96, 359.36, 335.08, 363.79, 332.65, 367.33, 337.07, 395.22, 367.39,
                395.44, 370.27, 396.77, 370.94, 395.0, 375.14, 392.34, 378.9, 399.2, 375.81, 400.75, 371.6, 401.2, 367.62, 396.99, 365.62, 394.56, 364.07, 369.99, 336.19,
                374.19, 335.97, 378.4, 337.52, 406.29, 364.52, 405.4, 366.29, 408.06, 369.17, 407.39, 372.26, 405.4, 376.03, 406.29, 377.35, 412.93, 370.05, 410.71, 364.3,
                406.95, 362.75, 380.39, 336.63, 385.26, 334.86, 413.59, 364.74, 415.14, 366.73, 416.25, 372.71, 415.8, 374.7, 420.67, 370.94, 418.46, 364.52, 415.14, 362.3,
                388.36, 336.41, 393.89, 335.97, 399.2, 339.29, 424.43, 362.97, 423.7, 366.33, 425.08, 368.23, 425.6, 363.06, 425.6, 360.47, 423.01, 360.3, 412.84, 350.12,
                405.08, 343.4, 400.94, 339.26, 398.35, 336.84, 402.66, 336.84, 405.94, 337.36, 417.67, 349.26, 425.43, 356.85, 424.74, 353.57, 412.49, 341.33, 408.53, 337.02,
                411.98, 336.84, 416.98, 341.16, 426.0, 348.57, 424.74, 344.09, 416.63, 337.53, 420.77, 336.5, 425.77, 336.33, 425.95, 319.43, 425.43, 314.6, 425.26, 314.6
            ],[   
                279.29, 269.61, 277.17, 269.59, 277.88, 267.57, 279.42, 266.51, 281.32, 267.22, 283.1, 267.1, 284.87, 268.17, 284.99, 270.3, 286.42, 271.96, 289.38, 274.45,
                288.91, 275.52, 286.42, 273.38, 283.57, 271.37, 281.79, 271.25, 280.49, 270.18], [311.32, 280.03, 311.09, 278.25, 310.97, 275.88, 307.77, 274.57, 304.56, 274.57,
                303.02, 276.35, 305.04, 278.25, 307.88, 279.08, 309.19, 280.5, 310.38, 282.52, 311.8, 281.21, 311.32, 279.43], [329.47, 356.59, 330.99, 363.26, 330.74, 367.02,
                327.73, 370.53, 323.22, 374.54, 327.48, 373.54, 331.74, 369.52, 331.24, 378.05, 334.01, 367.4, 335.71, 361.71, 333.88, 357.45, 332.71, 354.32, 330.95, 353.74,
                329.19, 356.47
            ]]
        ]
        x_min, x_max, y_min, y_max = Annotation.get_coords_from_segmentation(data)
        
        self.assertTrue(x_min > 0)
        self.assertTrue(x_max > 0)
        self.assertTrue(y_min > 0)
        self.assertTrue(y_max > 0)

    
    def test_get_coords_from_segmentation_second_dimension(self):
        x_min, x_max, y_min, y_max = Annotation.get_coords_from_segmentation([[10,10,20,10,20,20,10,20], [10,10,30,10,30,30,10,30]])
        self.assertEqual(x_min, 10)
        self.assertEqual(x_max, 30)
        self.assertEqual(y_min, 10)
        self.assertEqual(y_max, 30)


    def test_get_coords_from_segmentation_third_dimension(self):
        x_min, x_max, y_min, y_max = Annotation.get_coords_from_segmentation([[[10,10,20,10,20,20,10,20], [10,10,30,10,30,30,10,30]]])
        self.assertEqual(x_min, 10)
        self.assertEqual(x_max, 30)
        self.assertEqual(y_min, 10)
        self.assertEqual(y_max, 30)


    def test_save_annotation(self):
        annotation = Annotation.objects.create(image=self.image, category=self.category)
        
        result = Annotation.objects.all()[0]
        self.assertEqual(result.id, annotation.id)
        self.assertEqual(result.category, self.category)


    def test_save_boundingbox(self):
        boundingbox = Annotation.objects.create(image=self.image, category=self.category, x_min=10, y_min=10, x_max=20, y_max=20)
        result = Annotation.objects.all()[0]

        self.assertEqual(result.width, 10)
        self.assertEqual(result.height, 10)
        #self.assertEqual(result.area, 100)

        self.assertEqual(result.types(), ['annotation', 'boundingbox'])


    def test_save_segmentation(self):
        self.segmentation = Annotation.objects.create(image=self.image, category=self.category, segmentation=[10,10,20,10,20,20,10,20])
        
        result = Annotation.objects.all()[0]
        self.assertEqual(result.y_min, 10)
        self.assertEqual(result.x_min, 10)
        self.assertEqual(result.y_max, 20)
        self.assertEqual(result.x_max, 20)

        #self.assertEqual(result.area, 100)
        self.assertEqual(result.width, 10)
        self.assertEqual(result.height, 10)

        self.assertEqual(result.types(), ['annotation', 'boundingbox', 'segmentation'])
    

    def test_save_segmentation_multi(self):
        self.segmentation = Annotation.objects.create(image=self.image, category=self.category, segmentation=[[10,10,20,10,20,20,10,20]])
        
        result = Annotation.objects.all()[0]
        self.assertEqual(result.y_min, 10)
        self.assertEqual(result.x_min, 10)
        self.assertEqual(result.y_max, 20)
        self.assertEqual(result.x_max, 20)

        #self.assertEqual(result.area, 100)
        self.assertEqual(result.width, 10)
        self.assertEqual(result.height, 10)

        self.assertEqual(result.types(), ['annotation', 'boundingbox', 'segmentation'])


    def _create_some(self):
        self.annotation = Annotation.objects.create(image=self.image, category=self.category)
        self.boundingbox = Annotation.objects.create(image=self.image, category=self.category, x_min=10, y_min=10, x_max=20, y_max=20)
        self.segmentation = Annotation.objects.create(image=self.image, category=self.category, segmentation=[10,10,20,10,20,20,10,20])


    def test_find_annotation_scope(self):
        self._create_some()

        result = Annotation.objects.all()
        self.assertEqual(len(result), 3)
        self.assertEqual([ anno.id for anno in result], [self.annotation.id, self.boundingbox.id, self.segmentation.id])
        self.assertEqual(result[0].types(), ['annotation'])


    def test_find_boundingbox_scope(self):
        self._create_some()

        result = Annotation.boundingbox_objects.all()
        self.assertEqual(len(result), 2)
        self.assertEqual([ anno.id for anno in result], [self.boundingbox.id, self.segmentation.id])

        self.assertEqual(result[0].image, self.image)
        self.assertEqual(result[0].category, self.category)
        self.assertEqual(result[0].types(), ['annotation', 'boundingbox'])


    def test_find_segmentation_scope(self):
        self._create_some()

        result = Annotation.segmentation_objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual([ anno.id for anno in result], [self.segmentation.id])

        self.assertEqual(result[0].image, self.image)
        self.assertEqual(result[0].category, self.category)
        self.assertEqual(result[0].types(), ['annotation', 'boundingbox', 'segmentation'])
