from django.db import models

# Create your models here.

from django.shortcuts import render

# Create your views here.

# -*- coding: utf-8 -*-
import os
import re
import subprocess
import time

import psutil

# django 
from system_report.methods import percentage_to_grade

import subprocess

def get_gunicorn_workers():
    """
    For getting current workers in case of using gunicorn 
    """
    
    try:
        command = ["ps", "aux"]
        grep_gunicorn = subprocess.Popen(command, stdout=subprocess.PIPE)
        grep_filter = subprocess.Popen(["grep", "gunicorn"], stdin=grep_gunicorn.stdout, stdout=subprocess.PIPE)
        grep_gunicorn.stdout.close()
        grep_v_grep = subprocess.Popen(["grep", "-v", "grep"], stdin=grep_filter.stdout, stdout=subprocess.PIPE)
        grep_filter.stdout.close()
        wc_l = subprocess.Popen(["wc", "-l"], stdin=grep_v_grep.stdout, stdout=subprocess.PIPE)
        grep_v_grep.stdout.close()
        output = wc_l.communicate()[0].strip()
        return int(output.decode())
    except Exception as e:
        return f"Error: {e}"
        
class SystemMetrics(models.Model):
    """Class for the system metrics"""
    # _name = 'system.metrics'
    # _description = 'System Metrics'
    # _inherit = ['base.functions']

    # @api.model
    def get_system_metrics_data(self):
        """ Get CPU, Memory, Server, Process memory and disk performance Usage"""
        # cpu_usage = psutil.cpu_percent(interval=1)
        pid = os.getpid()
        process = psutil.Process(pid)
        cpu_grade = 0
        memory_grade = 0
        process_grade = 0
        disk_grade = 0

        # cpu utilization
        cpu_count = psutil.cpu_count()
        cpu_times = psutil.cpu_times_percent(interval=1)
        cpu_user_times = cpu_times.user
        cpu_system_times = cpu_times.system
        cpu_idle_times = cpu_times.idle
        cpu_iowait_times = cpu_times.iowait
        cpu_irq_times = cpu_times.irq
        load_avg = psutil.getloadavg()
        threshold_good = 0.7 * cpu_count

        # Get Memory Usage
        memory_info = process.memory_info()
        memory_info_rss = (memory_info.rss / (1024 ** 2))
        memory_info_vms = (memory_info.vms / (1024 ** 2))
        memory_info_shared = (memory_info.shared / (1024 ** 2))
        memory_info_text = (memory_info.text / (1024 ** 2))
        memory_info_data = (memory_info.data / (1024 ** 2))

        # server memory
        memory = psutil.virtual_memory()
        total_memory = memory.total / (1024.0 ** 2)
        cached_memory = (memory.cached / (1024 ** 2))
        buffered_memory = (memory.buffers / (1024 ** 2))
        shared_memory = (memory.shared / (1024 ** 2))

        storage = psutil.virtual_memory()
        used_ram_percent = storage.percent  # memory usage
        total_ram = round(storage.total / (1024.0 ** 2), 2)  # total memory
        used_mem = (total_ram * used_ram_percent) / 100
        free_mem = total_ram - used_mem

        allowed_workers = (cpu_count * 2) + 1
        current_workers = get_gunicorn_workers()
        # current_workers = tools.config['workers']
        min_cpu_count = (current_workers - 1) / 2

        # Disk performance
        initial = psutil.disk_io_counters()
        time.sleep(1)
        final = psutil.disk_io_counters()
        read_bytes = final.read_bytes - initial.read_bytes
        write_bytes = final.write_bytes - initial.write_bytes
        read_count = final.read_count - initial.read_count
        write_count = final.write_count - initial.write_count
        read_time = final.read_time - initial.read_time
        write_time = final.write_time - initial.write_time
        avg_response_time = (read_time + write_time) / (
                read_count + write_count) if (read_count + write_count) > 0 else 0
        total_throughput = read_bytes + write_bytes

        # Calculate IOPS
        total_iops = read_count + write_count
        # cpu utilization grading
        cpu_grade += 4 if cpu_user_times < 50 else (3 if cpu_user_times <= 70 else 2)
        cpu_grade += 4 if cpu_system_times < 30 else (3 if 30 <= cpu_system_times <= 50 else 2)
        cpu_grade += 4 if cpu_idle_times >= 50 else (3 if 30 <= cpu_idle_times < 50 else 2)
        cpu_grade += 4 if cpu_iowait_times < 10 else (3 if 10 <= cpu_iowait_times < 20 else 2)
        cpu_grade += 4 if current_workers < allowed_workers else (3 if current_workers > allowed_workers else 2)
        results = []
        for load in load_avg:
            if load <= threshold_good:
                results.append(4)
            elif threshold_good < load <= cpu_count:
                results.append(3)
            else:
                results.append(2)
        cpu_grade += sum(results)
        cpu_grade_per = (cpu_grade / 32) * 100
        cpu_rating = percentage_to_grade(cpu_grade_per)

        # Memory grading
        memory_grade += 4 if (used_mem <= (0.8 * total_memory)) else (3 if (
                (0.8 * total_memory) < used_mem <= (0.9 * total_memory)) else 2)
        memory_grade += 4 if (free_mem >= (0.2 * total_memory)) else (3 if (
                (0.1 * total_memory) < free_mem < (0.2 * total_memory)) else 2)
        memory_grade += 4 if shared_memory < (0.25 * total_memory) else (3 if (
                (0.25 * total_memory) <= shared_memory <= (0.5 * total_memory)) else 2)
        memory_grade += 4 if cached_memory < (0.5 * total_memory) else (3 if (
                (0.5 * total_memory) <= cached_memory <= (0.75 * total_memory)) else 2)
        memory_grade += 4 if buffered_memory < (0.5 * total_memory) else (3 if (
                (0.5 * total_memory) <= buffered_memory <= (0.75 * total_memory)) else 2)

        # total in percentage and it's grading
        memory_grade_per = (memory_grade / 20) * 100
        memory_rating = percentage_to_grade(memory_grade_per)

        # Process memory grading
        process_grade += 4 if (memory_info_rss <= (0.25 * total_memory)) else (3 if (
                (0.25 * total_memory) < memory_info_rss <= (0.5 * total_memory)) else 2)
        process_grade += 4 if (memory_info_vms <= (3 * memory_info_rss)) else (3 if (
                (3 * memory_info_rss) < memory_info_vms <= (5 * memory_info_rss)) else 2)
        process_grade += 4 if (memory_info_text <= 10) else (3 if (10 < memory_info_text <= 50) else 2)
        process_grade += 4 if (memory_info_shared <= 50) else (3 if (50 < memory_info_shared <= 200) else 2)
        process_grade += 4 if (memory_info_data <= 200) else (3 if (200 < memory_info_data <= 500) else 2)

        # total in percentage and it's grading
        process_grade_per = (process_grade / 20) * 100
        process_rating = percentage_to_grade(process_grade_per)

        # Disk memory grading
        disk_grade += 2 if (total_iops > 5000) else (3 if (3000 < total_iops <= 5000) else 4)
        disk_grade += 2 if (avg_response_time > 100) else (3 if (50 < avg_response_time <= 100) else 4)
        disk_grade += 2 if (total_throughput > (100 * 1024 * 1024)) else (3 if (
                (200 * 1024 * 1024) < total_throughput <= (100 * 1024 * 1024)) else 4)

        # total in percentage and it's grading
        disk_grade_per = (disk_grade / 12) * 100
        disk_rating = percentage_to_grade(disk_grade_per)

        return {'cpu_count': cpu_count,
                'cpu_user_times': cpu_user_times,
                'cpu_system_times': cpu_system_times,
                'cpu_idle_times': cpu_idle_times,
                'cpu_iowait_times': cpu_iowait_times,
                'cpu_irq_times': cpu_irq_times,
                'load_avg_1_min': round(load_avg[0], 2),
                'load_avg_5_min': round(load_avg[1], 2),
                'load_avg_15_min': round(load_avg[2], 2),
                'memory_info_rss': round(memory_info_rss, 2),
                'memory_info_vms': round(memory_info_vms, 2),
                'memory_info_shared': round(memory_info_shared, 2),
                'memory_info_text': round(memory_info_text, 2),
                'memory_info_data': round(memory_info_data, 2),
                'total_memory': round(total_memory, 2),
                'used_memory': round(used_mem, 2),
                'free_memory': round(free_mem, 2),
                'cached_memory': round(cached_memory, 2),
                'buffered_memory': round(buffered_memory, 2),
                'shared_memory': round(shared_memory, 2),
                'read_bytes': round(read_bytes, 2),
                'write_bytes': round(write_bytes, 2),
                'read_time': round(read_time, 2),
                'write_time': round(write_time, 2),
                'total_iops': round(total_iops, 2),
                'read_count': round(read_count, 2),
                'write_count': round(write_count, 2),
                'allowed_workers': allowed_workers,
                'current_workers': current_workers,
                'min_cpu_count': min_cpu_count,
                'cpu_grade': cpu_rating,
                'memory_grade': memory_rating,
                'process_grade': process_rating,
                'disk_grade': disk_rating,
                'avg_response_time': round(avg_response_time, 2),
                'total_throughput': total_throughput}


    # @api.model
    def get_server_uptime(self):
        """Get the server uptime."""
        result = subprocess.run(['uptime', '-p'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        uptime = result.stdout.decode('utf-8').strip()
        return {'uptime': uptime}


    # @api.model
    # def monitor_network_traffic(self, interval=1):
    #     """
    #     Monitors network traffic for all available interfaces and finds the most active one.
    #     :param interval: Time interval (in seconds) for monitoring.
    #     :return: Dictionary containing traffic details for all interfaces and the most active one.
    #     """
    #     net_io = psutil.net_io_counters(pernic=True)
    #
    #     if not net_io:
    #         return {'error': 'No network interfaces detected'}
    #
    #     # Capture initial values
    #     initial_stats = {iface: (data.bytes_recv, data.bytes_sent) for iface, data in net_io.items()}
    #
    #     time.sleep(interval)
    #
    #     # Capture new values
    #     new_net_io = psutil.net_io_counters(pernic=True)
    #     if not new_net_io:
    #         return {'error': 'Failed to retrieve updated network data'}
    #
    #     network_data = []
    #     for iface, (initial_recv, initial_sent) in initial_stats.items():
    #         if iface in new_net_io:
    #             final_recv = new_net_io[iface].bytes_recv
    #             final_sent = new_net_io[iface].bytes_sent
    #
    #             incoming_mb = (final_recv - initial_recv) / (1024 * 1024)
    #             outgoing_mb = (final_sent - initial_sent) / (1024 * 1024)
    #
    #             network_data.append({
    #                 'interface': iface,
    #                 'incoming_mb': round(incoming_mb, 2),
    #                 'outgoing_mb': round(outgoing_mb, 2)
    #             })
    #
    #     # Find the most active interface
    #     most_active = max(network_data, key=lambda x: x['incoming_mb'] + x['outgoing_mb'], default=None)
    #
    #     return {
    #         'network_traffic': network_data,
    #         'most_active_interface': most_active if most_active else {'error': 'No active interface detected'}
    #     }

    # @api.model
    # def get_odoo_network_interface(self):
    #     """
    #     Get the network interface Odoo is using.
    #     """
    #     # # Get Odoo's IP Address
    #     # hostname = socket.gethostname()
    #     # odoo_ip = socket.gethostbyname(hostname)
    #     # print("oo")
    #     #
    #     # # Find which network interface has this IP
    #     # for interface, addrs in psutil.net_if_addrs().items():
    #     #     for addr in addrs:
    #     #         if addr.family == socket.AF_INET and addr.address == odoo_ip:
    #     #             return {"interface": interface, "odoo_ip": odoo_ip}
    #     # print("lkjh",{"interface": interface, "odoo_ip": odoo_ip})
    #     #
    #     # return {"error": "Odoo network interface not found"}
    #
    #
    #     hostname = socket.gethostname()
    #     odoo_ip = socket.gethostbyname(hostname)
    #     net_io = psutil.net_io_counters(pernic=True)
    #     print("net_io,net_io")
    #
    #     # Ignore loopback (127.x.x.x)
    #     if odoo_ip.startswith("127."):
    #         print("kjh")
    #         return {"interface": "lo", "odoo_ip": odoo_ip}
    #
    #     # Find the real network interface
    #     for interface, addrs in psutil.net_if_addrs().items():
    #         for addr in addrs:
    #             if addr.family == socket.AF_INET and addr.address == odoo_ip:
    #                 return {"interface": interface, "odoo_ip": odoo_ip}
    #     print("oojhgfdsa",{"interface": interface, "odoo_ip": odoo_ip})
    #
    #     return {"error": "Odoo network interface not found"}
    #