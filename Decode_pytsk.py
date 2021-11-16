import pytsk3
import csv


class Decode():
    def __init__(self):
        """Creating the disk image variable which is equivalent to f=open()"""
        self.diskimage = pytsk3.Img_Info("DiskImage.001")
        self.volume_info = pytsk3.Volume_Info(self.diskimage)
        self.file_sys = pytsk3.FS_Info(self.diskimage)
        self.start_offsets = []
        self.__report_file = "Report.csv"

    def get_size(self):
        """
        Uses PyTSK get_size method to get the size in bytes
        then converts to megabytes
        """
        byte_size = self.diskimage.get_size()
        mb_size = round(byte_size/1000000, 2)
        return byte_size, mb_size

    def sector_count(self):
        """
        Uses PyTSK get_size method to get the size in bytes then
        divides by 512 (typical sector size) to find number  of
        sectors
        """
        byte_count = self.diskimage.get_size()
        sectors = byte_count/512
        return sectors

    def partition_table(self):
        print("There are", self.volume_info.info.part_count, "partitions in this image")

        count = 0
        for volume in self.volume_info:
            count += 1
            print("Partition number: ", count)
            print("Partition type: ", volume.desc.decode("ascii"))
            print("Start LBA: ", volume.start)
            print("Number of sectors: ", volume.len)
            print("")
            self.start_offsets.append(volume.start)
            self.report(count, volume.desc.decode("ascii"), volume.start, volume.len)
            self.fs_info()

    def fs_info(self):
        for start in self.start_offsets:
            a = self.file_sys.info(start)
            print(a)

    def report(self, num, type, start, sectors):
        with open(self.__report_file, 'a', newline='') as csvfile:
            linewriter = csv.writer(csvfile, delimiter='|',quotechar=chr(34), quoting=csv.QUOTE_MINIMAL)
            header = ["Number", "type", "Start", "Sectors" ]
            newline = ""
            info = [num, type, start, sectors]
            linewriter.writerow(header)
            linewriter.writerow(info)
            linewriter.writerow(newline)

    def main(self):
        while True:
            print("Options")
            print("1) Image size")
            print("2) Sector count")
            print("3 Decode partitions")
            print("4 Exit")
            prompt = input("Choose:\n")
            if prompt == "1":
                print(self.get_size())

            elif prompt == "2":
                print(self.sector_count())

            elif prompt == "3":
                self.partition_table()

            elif prompt == "4":
                quit()

            else:
                print("Invalid option chosen...")


if __name__ == '__main__':
    c = Decode()
    c.main()

