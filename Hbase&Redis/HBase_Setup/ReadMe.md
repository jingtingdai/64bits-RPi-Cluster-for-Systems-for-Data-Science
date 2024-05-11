# HBase Configuration

|       Directory      |                  Description                                    |
| :------------------- | :-------------------------------------------------------------- |
| Zookeeper_Setup.md   | Installation and configuration of Zookeeper                     |
| HBase_Setup.md       | Installation and configuration of HBase                         |

The above table reflects the order to set up HBase. ZooKeeper stores the HBase information, including the HBase metadata and HMaster addresses. Also, HBase is adatabase that runs on Hadoop cluster. Therefore, Zookeeper and Hadoop needs to be correctly installed and configured before HBase implementation. 