import navio.util
import navio.ublox

class GPS(object):
    def gpsData(self, x):
        ubl = navio.ublox.UBlox("spi:0.0", baudrate=5000000, timeout=2)

        ubl.configure_poll_port()
        ubl.configure_poll(navio.ublox.CLASS_CFG, navio.ublox.MSG_CFG_USB)
        #ubl.configure_poll(navio.ublox.CLASS_MON, navio.ublox.MSG_MON_HW)

        ubl.configure_port(port=navio.ublox.PORT_SERIAL1, inMask=1, outMask=0)
        ubl.configure_port(port=navio.ublox.PORT_USB, inMask=1, outMask=1)
        ubl.configure_port(port=navio.ublox.PORT_SERIAL2, inMask=1, outMask=0)
        ubl.configure_poll_port()
        ubl.configure_poll_port(navio.ublox.PORT_SERIAL1)
        ubl.configure_poll_port(navio.ublox.PORT_SERIAL2)
        ubl.configure_poll_port(navio.ublox.PORT_USB)
        ubl.configure_solution_rate(rate_ms=1000)

        ubl.set_preferred_dynamic_model(None)
        ubl.set_preferred_usePPP(None)

        ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_POSLLH, 1)
        ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_STATUS, 1)
        ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_SOL, 1)
        ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_VELNED, 1)
        ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_SVINFO, 1)
        ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_VELECEF, 1)
        ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_POSECEF, 1)
        ubl.configure_message_rate(navio.ublox.CLASS_RXM, navio.ublox.MSG_RXM_RAW, 1)
        ubl.configure_message_rate(navio.ublox.CLASS_RXM, navio.ublox.MSG_RXM_SFRB, 1)
        ubl.configure_message_rate(navio.ublox.CLASS_RXM, navio.ublox.MSG_RXM_SVSI, 1)
        ubl.configure_message_rate(navio.ublox.CLASS_RXM, navio.ublox.MSG_RXM_ALM, 1)
        ubl.configure_message_rate(navio.ublox.CLASS_RXM, navio.ublox.MSG_RXM_EPH, 1)
        ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_TIMEGPS, 5)
        ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_CLOCK, 5)
        #ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_DGPS, 5)

        while True:
            msg = ubl.receive_message()
            if msg is None:
                if opts.reopen:
                    ubl.close()
                    ubl = ublox.UBlox("spi:0.0", baudrate=5000000, timeout=2)
                print(empty)
            #print(msg.name())
            if msg.name() == "NAV_POSLLH":
                outstr = str(msg).split(",")[1:]
                outstr = "".join(outstr)
                outstrlen = len(outstr)
                #stripping values
                Long = outstr[11:21]
                Lat = outstr[31:40] 

                #handy output for visualization in this class, OW useless for data manip
                out = "Long:"+str(Long)+" Lat:"+str(Lat)

                Long = float(Long)
                Lat = float(Lat)
                
                if x == "lat":
                    return(float(Lat/10000000))
                if x == "lon":
                    return(float(Long/10000000))
                

