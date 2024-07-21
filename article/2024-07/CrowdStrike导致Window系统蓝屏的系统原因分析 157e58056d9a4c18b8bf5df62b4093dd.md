# CrowdStrike导致Window系统蓝屏的系统原因分析

Title: CrowdStrike导致Window系统蓝屏的系统原因分析

Date: 2024-7-23

Keywords: OperationSystem

---

2024年7月19日，全球范围内出现了CrowdStrike升级导致Window系统蓝屏的事件，蓝屏的直接原因是C++语言编写的程序引用了Null指针，但这个说法极尽推诿。就像一个人死了，他必然是大概率地失去了自主呼吸和心跳，但这些只是表面现象，何种原因导致了这种情况才是我们需要关心和解决的真正问题。

本文比较系统地解释了为何CrowdStrike出现的问题会导致系统蓝屏。换句话说，我们自己写的程序Null指针到处乱飞，它们除了让人着急以外，也不会导致系统蓝屏，但为什么CrowdStrike的Null指针却会造成如此重大的影响。

**CrowdStrike（CS）运行在哪里，认识Kernel Process**

- 要实现安全就要让渡权力，CS的安全策略（也是几乎所有安全软件的安全策略）都是要尽量多的掌握系统的底层情况。
- CS运行在Kernel Process中。像是套在系统驱动上的壳子，像家长控制孩子的手机验证一样，代理处理所有行为，实现系统行为的底层监控。

本文是搬运的一篇文章，英文太长我就不翻译了，只将重要的内容摘录如下。

**事件起因合理推测，CS的自动升级包有问题导致系统蓝屏**

- Unlike windows updates, Falcon Agent updates itself silently in the background. It gets the latest update from the cloud platform. As seen from the above architecture, the Falcon Agent gets the latest update, restarts and runs the latest version.
- The latest Agent might have a bug that might have written to Kernel’s memory causing corruption.

**CS的立即补救措施，发布升级补丁和用户自行删除**

- CrowdStrike mentioned the steps to mitigate the issue immediately. They deployed a fix and machines using the latest Agent wouldn’t face the same issue.
- They also stated that users should manually delete the faulty C-00000291*.sys file from the machines and reboot them. Similar workarounds are suggested for workloads running on cloud.

**As a software developer, key takeaways from this incident include:**

1. Before deployment, assess the impact of the change and the blast radius.
2. Adopt blue-green deployments to minimize the disruption to end-users.
3. Minimize the manual steps for users in case of software roll-backs. Roll-backs must be seamless, and user functionality shouldn’t get impacted.
4. When dealing with the OS kernel, follow best practices for testing and code reviews.
5. If developing an OS, use memory-safe languages like Rust over C/C++, and use concepts such as system extensions that limit a process’s access to the OS Kernel.

原文信息
19th July CrowdStrike Update: Blue Screen Havoc
Animesh Gaitonde12-15 minutes 7/20/2024
[Blue Screens to Blackouts: The Story Behind the CrowdStrike Outage](https://engineeringatscale.substack.com/p/blue-screens-to-blackouts-the-story)

---

[toc]

## Brief

On 19th July 2024, the world witnessed one of the biggest IT disruptions in recent years. Corporations worldwide reported outages and disruptions, with Windows computers displaying the dreaded Blue Screen of Death (BSOD) Error.

The outage impacted sectors such as airlines, banking, trading, media companies and many more. It was confirmed that there was no security incident or cyberattack resulting in this disruption.

The outage was due to a software update of Falcon, a tool built by the cybersecurity firm CrowdStrike. The latest update resulted in a crash of Windows operating system and resulted in worldwide outage.

In this article, we will dive deep and understand the issue. We will start by demystifying the Blue Screen of Death by revisiting the operating system fundamentals. Later, we will look at CrowdStrike’s architecture, the faulty release and the mitigation strategy. We will conclude by going over some key learnings from this incident.

## Blue Screen of Death (BSOD)

If you use Windows, you've likely encountered the Blue Screen of Death (BSOD). This error screen indicates that the system has malfunctioned, usually due to hardware or software issues.

After the reboot, everything works seamlessly. But, do you know why the BSOD appears ? And why does it appear only on Windows machine and not on Linux/Mac ? Let’s understand this in detail.

Before going into the details, we will revisit some operating system concepts. This would help us grasp complex details in an easy manner. The operating system manages hardware components like memory, CPU, and I/O devices, with the Kernel at its core.

The Kernel is responsible for primary functionalities such as :

1. `Memory management` - Allocating/Deallocating memory for the running processes. Tracking the memory used by the processes.
2. `Process management` - Managing the process lifecycle and ensuring two or more processes run in the memory without any issue.
3. `Device management` - Communication with devices like monitor, mouse, keyboard, printers, etc.
4. `File System management` - Organizing the files on the hard drive or any external storage.

The processes running on any computer/machine run in two modes - a) `Kernel Mode` b) `User Mode`.

### Kernel Mode

This mode has highest privilege and can directly interact with all the hardware. Operating system processes run in this mode.

It’s a critical mode and any errors in the code can result in system instability and eventual crash. Hence, code has to be written meticulously and should be error-free.

As users, we don’t directly deal with processes that run in the kernel mode. However, you can view them in the Windows Task Manager. The following snippet shows processes such as Host processes and NT Kernel & System running in kernel mode.

![Windows Task Manager listing running processes](CrowdStrike%E5%AF%BC%E8%87%B4Window%E7%B3%BB%E7%BB%9F%E8%93%9D%E5%B1%8F%E7%9A%84%E7%B3%BB%E7%BB%9F%E5%8E%9F%E5%9B%A0%E5%88%86%E6%9E%90%20157e58056d9a4c18b8bf5df62b4093dd/Untitled.png)

Windows Task Manager listing running processes

### User Mode

The user mode has least privilege and it can’t directly interact with the hardware. It uses the operating system to get the data from any hardware device.

The user mode processes call system calls for sending/receiving data to/from the hardware. For example: User programs call fopen system call to open a file on the hard disk.

The operating system ensures that the user process doesn’t access any memory that’s not assigned to it. In case a user process accesses memory belonging to a different process or a kernel process, the operating system sends a SIGSEV to the process. And the process finally terminates and the user sees a SEGFAULT (Segmentation Fault).

![User process accessing Kernel’s memory](CrowdStrike%E5%AF%BC%E8%87%B4Window%E7%B3%BB%E7%BB%9F%E8%93%9D%E5%B1%8F%E7%9A%84%E7%B3%BB%E7%BB%9F%E5%8E%9F%E5%9B%A0%E5%88%86%E6%9E%90%20157e58056d9a4c18b8bf5df62b4093dd/Untitled%201.png)

User process accessing Kernel’s memory

Applications that you use daily such as web browsers, MS Excel, MS Word, games, media players like VLC, etc run in user mode.

### What causes BSOD ?

BSOD is only shown for Windows devices. It indicates that the system has malfunctioned. It could be either due to a hardware or software issue. The following are few reasons for BSOD :

1. `File system corruption` - In case the files required by the Kernel are corrupted, the system can crash.
2. `Device driver issues` - Incompatible or corrupted device drivers can lead to communication errors. And eventually cause BSOD.
3. `Software bugs` - Bugs which modify critical Kernel data structures, and access forbidden memory locations can bring the system to a halt.
4. `Malware` - Malware can interfere with the system processes leading to a BSOD.

In most of the cases, we restart the system and as expected it starts functioning. We can often troubleshoot the issue by looking at the system logs. To ensure smooth functioning of operating system, it is essential to prevent scenarios such as kernel’s data corruption, accidental modification of kernel’s memory, etc. Mac/Linux use different Kernel, data structures and error handling mechanisms. In case of an OS crash, both OSs use Kernel panic. Unlike Windows’s BSOD, Mac/Linux show a screen with error messages.

Now, that you understand BSOD, let’s understand the reason for 19th July’s worldwide BSOD.

## 19th July’s BSOD

72% of the users in the world are windows users. Windows devices use tools developed by CrowdStrike(CRWD) for cybersecurity. CrowdStrike has developed a suite of cloud-native tools. One such product in their suite is known as `CrowdStrike Falcon`. CrowdStrike Falcon offers the following features :

1. Endpoint security - It detects and prevents malware, ransomware and other threats.
2. Extended detection and response (XDR) - Helps in investigating security incidents, identifying root causes, and taking the right steps.
3. Cloud workload protection - It monitors any malicious activity in cloud environments for Azure, AWS , and Google Cloud Platform (GCP).

### CrowdStrike Falcon architecture

Falcon is installed on all the devices and runs as an agent (sensor). It continuously monitors the device activity.

CrowdStrike runs a cloud platform that collects data from all the Falcon agents. This platform also serves as a control plane for CrowdStrike to view the threats and security incidents.

Falcon agents run as background processes. They collect the security data from the device and send it to the CrowdStrike platform.

The following image shows the architecture (for representation only) of Falcon :

![Falcon’s architecture (for representation only)](CrowdStrike%E5%AF%BC%E8%87%B4Window%E7%B3%BB%E7%BB%9F%E8%93%9D%E5%B1%8F%E7%9A%84%E7%B3%BB%E7%BB%9F%E5%8E%9F%E5%9B%A0%E5%88%86%E6%9E%90%20157e58056d9a4c18b8bf5df62b4093dd/Untitled%202.png)

Falcon’s architecture (for representation only)

Falcon Agent runs as a kernel process since it has to monitor activities such as -

- Device driver activity
- Network traffic
- Restricted file accesses

The above activities require highest privileges and as a result, the Falcon Agent runs in a kernel mode.

**Unlike windows updates, Falcon Agent updates itself silently in the background. It gets the latest update from the cloud platform. As seen from the above architecture, the Falcon Agent gets the latest update, restarts and runs the latest version.**

### Faulty deployment

Recently, CrowdStrike deployed latest version of Falcon Agent. The file C-00000291*.sys was updated and the running agents downloaded the file. After consuming the update, windows machines started crashing. The issue wasn’t observed on the machines where the agent wasn’t updated.

This was observed worldwide and brought most of the economic activities such as Air travel, Hospitals, Stock trading, etc to a standstill. CrowdStrike discovered that the issue was due to faulty update in the C-00000291*.sys file. A fix was deployed and the file C-00000291*.sys with timestamp of 0527 UTC had the fix. While the one with 0409 UTC was the problematic one. Reference - [Falcon update for Windows host](https://www.crowdstrike.com/blog/statement-on-falcon-content-update-for-windows-hosts/).

CrowdStrike hasn’t published the exact technical details. However, I suspect it could be due to incompatibility between the latest agent update and it’s interaction with the Kernel.

**The latest Agent might have a bug that might have written to Kernel’s memory causing corruption.** This might have resulted in the crash. And since this was repetitive, the fault might have been in Falcon Agent’s initialization.

![Process illustrating BSOD after Falcon Agent update (for representation only)](CrowdStrike%E5%AF%BC%E8%87%B4Window%E7%B3%BB%E7%BB%9F%E8%93%9D%E5%B1%8F%E7%9A%84%E7%B3%BB%E7%BB%9F%E5%8E%9F%E5%9B%A0%E5%88%86%E6%9E%90%20157e58056d9a4c18b8bf5df62b4093dd/Untitled%203.png)

Process illustrating BSOD after Falcon Agent update (for representation only)

### Immediate Fix

CrowdStrike mentioned the steps to mitigate the issue immediately. They deployed a fix and machines using the latest Agent wouldn’t face the same issue.

They also stated that users should manually delete the faulty C-00000291*.sys file from the machines and reboot them. Similar workarounds are suggested for workloads running on cloud.

According to me, it would take a couple of days for the fix to reach all the machines worldwide. Also, since it requires manual intervention, non-technical users would face a challenge. But, hopefully, it will get resolved soon.

## Long-term mitigation

On 19th July, we witnessed how a simple software update can disrupt our daily life. In the future, such issues must be avoided at all costs.In my opinion, there are two angles to the 19th July’s BSOD issue :

1. `Agent updates` - The issue could have been prevented if the update wasn’t rolled out to all the users.
2. `OS design` - Linux/Mac didn’t face the same issue. However, it impacted most of the Windows devices. A better design of OS and its kernel modules would have prevented this havoc.

### Agent updates

Since the agents are installed on the end-user devices, it makes the deployment more challenging. Unlike cloud-services, these changes can’t be rolled-back automatically. And also the blast radius is huge as it encompasses all devices in the world.

However, in the future, CrowdStrike can follow a strategy similar to blue-green deployment. Instead of all the agents receiving the update, a set of computers (green environment) would receive the update. It would bake for few days in the green environment and then the change would roll-out to the blue environment (end-user devices).

Similarly, since the Agent runs in the kernel mode, the testing must be rigorous. Also, the code reviews must be done thoroughly and critically. There should be enough guardrails to prevent any accidental updates to the source operating system.

### OS design

Windows users have a history of dealing with BSOD. Over the years, Windows has become stable and users are seeing BSOD less frequently.

One of the primary reasons for BSOD can be attributed to the design of Windows OS. While kernel extensions provide low-level access, hardware interaction and customization, the downside is instability.

Mac followed a similar approach until macOS 10.15 (Catalina). Since then, Mac introduced system sxtensions. System extensions run as User processes and have limited access to the core kernel. This prevents unexpected crashes, and reduces security vulnerabilities.

Windows can benefit from following Mac’s footsteps in the future. It would improve overall security and stability.

Additionally, the Windows kernel is implemented in C/C++. These languages are prone to errors such as buffer overflows, dangling pointers, & Null pointer references. The errors lead to process crashes.

Microsoft has started rewriting its kernel in Rust. Rust’s strong typing and ownership system make it memory safe. In the future, 19th July-like BSOD issues can be prevented with the Windows version written in Rust.

## Conclusion

On 19th July, the majority of systems running Windows faced BSOD. Moreover, cloud services running on Windows servers were impacted, disrupting many clients relying on these services.

The root cause of the issue was a faulty update of CrowdStrike’s Falcon Agent (sensor). The latest update caused an OS crash, and users started seeing BSOD.

CrowdStrike identified the issue and rolled out a fix. They also suggested ways to mitigate the issues on their website. Some users had to manually reboot their machines and delete the problematic file from the update as an immediate fix. In a couple of days, all systems are expected to function normally.

As a software developer, key takeaways from this incident include :

1. Before deployment, assess the impact of the change and the blast radius.
2. Adopt blue-green deployments to minimize the disruption to end-users.
3. Minimize the manual steps for users in case of software roll-backs. Roll-backs must be seamless, and user functionality shouldn’t get impacted.
4. When dealing with the OS kernel, follow best practices for testing and code reviews.
5. If developing an OS, use memory-safe languages like Rust over C/C++, and use concepts such as system extensions that limit a process’s access to the OS Kernel.

## Reference

1. [CrowdStrike Statement on Falcon Content Update for Windows Hosts](https://www.crowdstrike.com/blog/statement-on-falcon-content-update-for-windows-hosts/)
2. [CrowdStrike update causes major global IT outage](https://techcrunch.com/2024/07/19/faulty-crowdstrike-update-causes-major-global-it-outage-taking-out-banks-airlines-and-businesses-globally/)
