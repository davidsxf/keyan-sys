import json
import requests
from datetime import datetime

# 设置基础URL
base_url = "http://localhost:8000/api/v1"

# 测试用的项目ID和员工ID（请根据实际数据修改）
test_project_id = 1  # 确保这个项目ID存在
test_staff_id = 1    # 确保这个员工ID存在
created_participant_id = None  # 用于存储创建的参与人员ID

# 辅助函数：打印响应信息
def print_response(response):
    print(f"状态码: {response.status_code}")
    try:
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except json.JSONDecodeError:
        print(f"响应内容: {response.text}")
    print("=" * 50)

# 测试1: 获取项目参与人员角色选项
def test_get_participant_roles():
    print("\n测试1: 获取项目参与人员角色选项")
    url = f"{base_url}/projects/participants/roles"
    response = requests.get(url)
    print_response(response)
    return response.json() if response.status_code == 200 else None

# 测试2: 创建项目参与人员
def test_create_project_participant():
    global created_participant_id
    print("\n测试2: 创建项目参与人员")
    url = f"{base_url}/projects/participants"
    data = {
        "project_id": test_project_id,
        "staff_id": test_staff_id,
        "role": "member",
        "order": 1,
        "join_date": datetime.now().strftime("%Y-%m-%d"),
        "remark": "测试参与人员"
    }
    response = requests.post(url, json=data)
    print_response(response)
    if response.status_code == 200:
        created_participant_id = response.json().get("id")
        print(f"创建成功，参与人员ID: {created_participant_id}")
    else:
        print(f"创建失败，响应码: {response.status_code}")
    return response

# 测试3: 获取项目参与人员列表
def test_list_project_participants():
    print("\n测试3: 获取项目参与人员列表")
    url = f"{base_url}/projects/participants"
    # 可以添加查询参数进行筛选
    params = {
        "project_id": test_project_id
    }
    response = requests.get(url, params=params)
    print_response(response)
    return response

# 测试4: 获取单个项目参与人员详情
def test_get_project_participant():
    print("\n测试4: 获取单个项目参与人员详情")
    if not created_participant_id:
        print("跳过测试，没有创建的参与人员ID")
        print("=" * 50)
        return None
    url = f"{base_url}/projects/participants/{created_participant_id}"
    response = requests.get(url)
    print_response(response)
    return response

# 测试5: 更新项目参与人员信息
def test_update_project_participant():
    print("\n测试5: 更新项目参与人员信息")
    if not created_participant_id:
        print("跳过测试，没有创建的参与人员ID")
        print("=" * 50)
        return None
    url = f"{base_url}/projects/participants/{created_participant_id}"
    data = {
        "project_id": test_project_id,
        "staff_id": test_staff_id,
        "role": "advisor",  # 更改角色
        "order": 2,
        "remark": "更新后的测试参与人员"
    }
    response = requests.put(url, json=data)
    print_response(response)
    return response

# 测试6: 获取指定项目的所有参与人员
def test_list_participants_by_project():
    print("\n测试6: 获取指定项目的所有参与人员")
    url = f"{base_url}/projects/{test_project_id}/participants"
    response = requests.get(url)
    print_response(response)
    return response

# 测试7: 删除项目参与人员
def test_delete_project_participant():
    print("\n测试7: 删除项目参与人员")
    if not created_participant_id:
        print("跳过测试，没有创建的参与人员ID")
        print("=" * 50)
        return None
    url = f"{base_url}/projects/participants/{created_participant_id}"
    response = requests.delete(url)
    print_response(response)
    return response

# 运行所有测试
def run_all_tests():
    print("开始测试ProjectStaff API...")
    
    # 获取角色选项
    roles = test_get_participant_roles()
    
    # 创建参与人员
    create_response = test_create_project_participant()
    
    # 获取参与人员列表
    list_response = test_list_project_participants()
    
    # 获取单个参与人员详情
    get_response = test_get_project_participant()
    
    # 更新参与人员信息
    update_response = test_update_project_participant()
    
    # 获取指定项目的参与人员
    list_by_project_response = test_list_participants_by_project()
    
    # 删除参与人员
    delete_response = test_delete_project_participant()
    
    print("测试完成！")

if __name__ == "__main__":
    run_all_tests()