import pandas as pd
import random

if __name__ == '__main__':
    # 生成员工ID池（EMP001-EMP300）
    employee_pool = [f"EMP{str(i).zfill(3)}" for i in range(1, 301)]

    # 生成客户ID池（CUST001-CUST100）
    customer_pool = [f"CUST{str(i).zfill(3)}" for i in range(1, 101)]

    # 生成随机数据
    data = {
        "Employee_ID": random.choices(employee_pool, k=5000),
        "Customer_ID": random.choices(customer_pool, k=5000)
    }

    # 创建DataFrame
    df = pd.DataFrame(data)
    df.to_csv('111.csv')


    # 验证数据
    print(f"总行数：{len(df)}")
    print(f"实际员工ID数量：{df['Employee_ID'].nunique()}")
    print(f"实际客户ID数量：{df['Customer_ID'].nunique()}")
    print("\n前5行数据示例：")
    print(df.head())