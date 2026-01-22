
## table

+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Rule ID | Rule Text (As Specified in SBMR)                                                                                                                                                                                 |
+=========+==================================================================================================================================================================================================================+
| M3_SB_1 | SBMR standardizes the side-band interface based on the DMTF PMCI workgroup standards which define specifications for primary intercommunication interfaces and data models between BMC and SatMC.                |
+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| M3_SB_2 | PLDM is used for the purpose of supporting platform-level data models and platform functions.                                                                                                                    |
+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| M3_SB_3 | MCTP is used as a transport protocol format that is independent of the underlying physical bus properties, as well as the “data-link” layer messaging used on the bus.                                           |
+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| M3_SB_4 | PLDM over MCTP binding is used as the format of PLDM over MCTP messages.                                                                                                                                         |
+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| M3_SB_5 | SPDM is used for the purpose of supporting security related capabilities of the devices.                                                                                                                         |
+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| M3_SB_6 | SPDM over MCTP binding is used as the format of SPDM over MCTP messages.                                                                                                                                         |
+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| M3_SB_7 | Secure messages using SPDM specifications is used for the purpose of supporting secure transfer of application data over PMCI transports using SPDM. Secure messages also define the transport requirements for  |
|         | SPDM records, which form the basis of encryption and message authentication.                                                                                                                                     |
+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| M3_SB_8 | Secured Messages using SPDM over MCTP binding is used as the format of SPDM secure messages over MCTP messages.                                                                                                  |
+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| M3_SB_9 | The physical and data-link layer methods for MCTP communication are minimally defined by the MCTP over SMBus/I2C binding specification. This interface must support bi-directional transfer of MCTP packets,     |
|         | which requires that both sides of the communication have completer addresses. Implementations may choose a higher bandwidth physical data-link, such as MCTP over PCIe VDM or MCTP over I3C.                     |
+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| M4_SB_1 | The physical and data-link layer methods for MCTP communication are defined by the MCTP over I3C binding specification.                                                                                          |
+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
