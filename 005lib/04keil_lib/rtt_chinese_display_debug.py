#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文RTT实时显示 - 最终修复版
修复了错误代码 -11 (RTT缓冲区溢出) 问题
"""

import pylink
import sys
import time
import traceback
from datetime import datetime

# ==================== 配置 ====================
DEVICE = "HC32F460xE"
INTERFACE = "SWD"
SPEED = 10000  # kHz
RTT_CHANNEL = 0
BUFFER_SIZE = 4096

# 可选：同时保存到文件
SAVE_TO_FILE = True
LOG_FILE = f"RTT_Log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
# =============================================

def pause():
    """暂停等待用户按键"""
    input("\n按回车键退出...")

def main():
    print("=" * 60)
    print("中文RTT实时显示 - 最终修复版")
    print("=" * 60)
    print()
    
    jlink = None
    log_fp = None
    error_count = 0
    max_errors = 10  # 连续错误次数上限
    
    try:
        # 步骤1: 初始化JLink
        print("[1/4] 初始化JLink...")
        jlink = pylink.JLink()
        print("  ✓ JLink对象创建成功")
        
        # 步骤2: 打开连接
        print("[2/4] 连接J-Link调试器...")
        jlink.open()
        print("  ✓ JLink已打开")
        
        # 步骤3: 设置接口和连接设备
        print(f"[3/4] 连接目标设备: {DEVICE}...")
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE, speed=SPEED)
        print(f"  ✓ 已连接到: {DEVICE}")
        print(f"  ✓ 接口: SWD, 速度: {SPEED}kHz")
        
        # 步骤4: 启动RTT
        print("[4/4] 启动RTT...")
        jlink.rtt_start()
        print("  ✓ RTT已启动")
        print()
        print("=" * 60)
        print("✓ 连接成功！中文RTT实时显示运行中...")
        print("  按 Ctrl+C 停止")
        print("=" * 60)
        print()
        
        # 打开日志文件
        if SAVE_TO_FILE:
            log_fp = open(LOG_FILE, 'w', encoding='utf-8')
            log_fp.write(f"RTT Log Started: {datetime.now()}\n")
            log_fp.write("=" * 50 + "\n")
            print(f"[日志] 同时保存到: {LOG_FILE}")
            print()
        
        # 实时读取循环
        while True:
            try:
                # 读取RTT数据（返回的是整数列表）
                data_list = jlink.rtt_read(RTT_CHANNEL, BUFFER_SIZE)
                
                # 关键修复：pylink返回的是整数列表，需要转换为bytes
                if data_list and len(data_list) > 0:
                    # 将整数列表转换为bytes，再解码为UTF-8
                    data_bytes = bytes(data_list)
                    text = data_bytes.decode('utf-8', errors='replace')
                    
                    # 实时显示
                    print(text, end='', flush=True)
                    
                    # 写入文件
                    if log_fp:
                        log_fp.write(text)
                        log_fp.flush()
                    
                    # 成功读取后重置错误计数
                    error_count = 0
                
                # 关键修复：减少延迟，防止缓冲区溢出
                # 从1ms改为0.1ms，提高读取频率
                time.sleep(0.0001)
                
            except KeyboardInterrupt:
                print("\n\n[用户中断]")
                break
                
            except pylink.errors.JLinkRTTException as e:
                # 关键修复：捕获RTT错误（包括错误代码-11），忽略并继续
                error_count += 1
                if error_count > max_errors:
                    print(f"\n[警告] 连续{max_errors}次读取错误，可能是目标板已断开")
                    break
                # 短暂延迟后继续
                time.sleep(0.01)
                continue
                
            except Exception as e:
                # 其他未知错误
                print(f"\n[警告] 读取异常: {e}")
                error_count += 1
                if error_count > max_errors:
                    raise
                time.sleep(0.01)
                continue
                
    except pylink.errors.JLinkException as e:
        print(f"\n[错误] JLink异常: {e}")
        print("\n可能的原因:")
        print("  1. J-Link调试器未连接")
        print("  2. 目标板未上电")
        print("  3. 目标板未运行RTT程序")
        print("  4. 芯片型号不匹配")
        traceback.print_exc()
        pause()
        
    except Exception as e:
        print(f"\n[错误] 未知异常: {e}")
        traceback.print_exc()
        pause()
        
    finally:
        # 清理资源
        print("\n[清理资源...]")
        
        if log_fp:
            try:
                log_fp.close()
                print(f"  ✓ 日志已保存: {LOG_FILE}")
            except:
                pass
        
        if jlink:
            try:
                jlink.rtt_stop()
                print("  ✓ RTT已停止")
            except:
                pass
            try:
                jlink.close()
                print("  ✓ JLink已关闭")
            except:
                pass
        
        print("\n[程序结束]")
        pause()

if __name__ == "__main__":
    main()