from pico_rtc_u2u_sd_gpio import i2c1



class eDog:
    def __init__(self, ):    
         self.offs = 0
         self.buff_len = 16
         self.buff = [0]*self.buff_len
         
    def put_tx_buff_u32(self, u32):
        self.buff[self.offs] = (u32 >> 24) & 0xFF
        self.offs = self.offs + 1 
        self.buff[self.offs] = (u32 >> 16) & 0xFF
        self.offs = self.offs + 1 
        self.buff[self.offs] = (u32 >> 8) & 0xFF
        self.offs = self.offs + 1 
        self.buff[self.offs] = u32 & 0xFF
        self.offs = self.offs + 1 
        
        
    def put_tx_buff_u16(self, u16):
        self.buff[self.offs] = (u16 >> 8) & 0xFF
        self.offs = self.offs + 1 
        self.buff[self.offs] = u16 & 0xFF
        self.offs = self.offs + 1 

    def put_tx_buff_u82(self, u8):
        self.buff[self.offs] = u8 & 0xFF
        self.offs = self.offs + 1 


    def print_buff(self, start):
        indx = start
        n = 0
        while n < self.buff_len:
            print('{:02X} '.format(self.buff[start + n]),end='')
            n = n + 1      
                  
            
    
ed = eDog()
ed.put_tx_buff_u32(1234)
print(ed.buff)
ed.print_buff(0)
                  
                  
                  
                  