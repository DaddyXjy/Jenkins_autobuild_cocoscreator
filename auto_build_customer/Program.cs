using System;
using System.Collections.Generic;
using System.Collections;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;
using System.IO;
using System.Xml;
using System.Text.RegularExpressions;
using System.Diagnostics;
using System.Threading;
using System.Runtime.Serialization.Formatters.Binary;

namespace deleteUnuseAssets
{
    class Program
    {
        static HashSet<string> mapDfs = new HashSet<string>();
        static Dictionary<string, string> uuidToFile = new Dictionary<string, string>();
        static List<FileInfo> assetsFiles = new List<FileInfo>();
        static string resourcePath = "";
        static string commonStatic = "";
        public static void getAllFiles(string dirName, List<FileInfo> arrAllFiles, List<string> extensions = null)
        {
            var folder = new DirectoryInfo(dirName);
            foreach (var file in folder.GetFiles())
            {
                if (extensions == null || extensions.Contains(file.Extension))
                {
                    arrAllFiles.Add(file);
                }
            }
            foreach (var fo in folder.GetDirectories())
            {
                getAllFiles(fo.FullName, arrAllFiles, extensions);
            }
        }
        public static bool findInFileArr(List<FileInfo> arrimportFiles, string str)
        {
            foreach (var it in arrimportFiles)
            {
                var fileText = File.ReadAllText(it.FullName);
                if (fileText.IndexOf(str) != -1)
                {
                    return true;
                }
            }
            return false;
        }
        static void Main(string[] args)
        {
            var folderPath = args[0];
            var customerMark = "";
            if (args.Count() > 1)
            {
                customerMark = args[1];
            }
            var folder = new DirectoryInfo(folderPath);
            var assetsFolder = Path.Combine(folder.FullName, "assets");
            var assetsFolderInfo = new DirectoryInfo(assetsFolder);
            resourcePath = Path.Combine(folder.FullName, "assets", "resources");
            commonStatic = Path.Combine(folder.FullName, "assets", "CommonStaticAssets");
            var allDirs = assetsFolderInfo.GetDirectories("*", SearchOption.AllDirectories);
            foreach (var it in allDirs)
            {
                if (it.Name.ToLower() == "designsketch")
                {
                    Directory.Delete(it.FullName, true);
                }
            }
            getAllFiles(assetsFolder, assetsFiles);
            foreach (var it in assetsFiles)
            {
                if (it.Name.IndexOf(' ') != -1)
                {
                    Console.WriteLine("Error:file {0} has space", it.FullName);
                }
            }
            if (customerMark == "test102")
            {
                customerMark = "master";
            }
            //if (customerMark != "")
            //{
            //    bool find = false;
            //    foreach (var it in assetsFiles)
            //    {
            //        if (it.Name == "Loading_" + customerMark + ".fire")
            //        {
            //            find = true;
            //            break;
            //        }
            //    }
            //    if (!find)
            //    {
            //        customerMark = "master";
            //    }
            //}
            for (var i = assetsFiles.Count() - 1; i >= 0; --i)
            {
                var it = assetsFiles[i];
                if (it.Name == "EmotionTest.fire" || it.Name == "PolygonTest.fire" || it.Name == "WayBillTest.fire" 
                    || it.Name == "LuDanTest.fire" || it.Name == "EmotionTest.fire.meta" || it.Name == "PolygonTest.fire.meta"
                    || it.Name == "WayBillTest.fire.meta" || it.Name == "LuDanTest.fire.meta")
                {
                    File.Delete(it.FullName);
                    assetsFiles.RemoveAt(i);
                }
                else if (customerMark != "" && Regex.IsMatch(it.Name, @"(Loading|Login|MenuScene|Video)_\w+\.fire(.meta)?$")
                    && !it.Name.Contains(customerMark))
                {
                    File.Delete(it.FullName);
                    assetsFiles.RemoveAt(i);
                }
            }
            foreach (var file in assetsFiles)
            {
                if (file.Extension == ".meta")
                {
                    var text = File.ReadAllText(file.FullName);
                    foreach (var p in Regex.Matches(text, @"""uuid""\s*:\s*""([^""]+)").Cast<Match>())
                    {
                        var uuid = p.Result("$1");
                        if (uuidToFile.ContainsKey(uuid) && uuidToFile[uuid] != file.FullName)
                        {
                            Console.WriteLine(string.Format("uuid重复:{0}, {1}", file.FullName, uuidToFile[uuid]));
                        }
                        var fileName = file.FullName.Substring(0, file.FullName.Length - 5);
                        uuidToFile[uuid] = fileName;
                    }
                }
            }
            foreach (var it in assetsFiles)
            {
                if (it.Extension == ".fire" || (it.FullName.IndexOf(resourcePath) == 0 && it.Extension != ".jpg" && it.Extension != ".png" && it.Extension != ".mp3"))
                {
                    dfs(it.FullName);
                }
            }
            var pacFiles = new List<FileInfo>();
            var pacFilesSet = new HashSet<string>();
            foreach (var fileInfo in assetsFiles)
            {
                if (fileInfo.FullName.IndexOf(resourcePath) == -1 && fileInfo.Extension == ".pac")
                {
                    getAllFiles(fileInfo.DirectoryName, pacFiles);
                }
            }
            foreach (var it in pacFiles)
            {
                pacFilesSet.Add(it.FullName);
            }
            var otherThanPac = new List<FileInfo>();
            foreach (var it in assetsFiles)
            {
                if ((it.Extension == ".png" || it.Extension == ".jpg" || it.Extension == ".mp3") && it.FullName.IndexOf(resourcePath) == -1 && !pacFilesSet.Contains(it.FullName))
                {
                    otherThanPac.Add(it);
                }
            }
            Console.WriteLine("delete unuse AutoAtlas image:");
            foreach (var fileInfo in pacFiles)
            {
                if (fileInfo.Extension == ".jpg" || fileInfo.Extension == ".png")
                {
                    if (!mapDfs.Contains(fileInfo.FullName))
                    {
                        Console.WriteLine("delete unuse image:{0}", fileInfo.FullName);
                        File.Delete(fileInfo.FullName);
                        File.Delete(fileInfo.FullName + ".meta");
                    }
                }
            }
            foreach (var fileInfo in pacFiles)
            {
                if (fileInfo.Extension == ".pac")
                {
                    var tmpArr = new List<FileInfo>();
                    getAllFiles(fileInfo.DirectoryName, tmpArr, new List<string> { ".png", ".jpg" });
                    if (tmpArr.Count() == 0)
                    {
                        Console.WriteLine("delete unuse AutoAtlas:{0}", fileInfo.FullName);
                        File.Delete(fileInfo.FullName);
                        File.Delete(fileInfo.FullName + ".meta");
                    }
                }
            }
            //其他的未用到的资源
            Console.WriteLine("find these picture unused in project:");
            foreach (var fileInfo in otherThanPac)
            {
                if (!mapDfs.Contains(fileInfo.FullName) && fileInfo.FullName.IndexOf(commonStatic) == -1)
                {
                    Console.WriteLine("unused picture:{0}", fileInfo.FullName);
                    //File.Delete(fileInfo.FullName);
                    //File.Delete(fileInfo.FullName + ".meta");
                }
            }
        }
        static void dfs(string fullName)
        {
            mapDfs.Add(fullName);
            if (fullName.IndexOf(".png") == fullName.Length - 4 || fullName.IndexOf(".jpg") == fullName.Length - 4 || fullName.IndexOf(".mp3") == fullName.Length - 4)
            {
                return;
            }
            if (!File.Exists(fullName))
            {
                return;
            }
            var text = File.ReadAllText(fullName);
            foreach (var p in Regex.Matches(text, @"\b\w{8}-\w{4}-\w{4}-\w{4}-\w{12}\b").Cast<Match>())
            {
                var uuid = p.ToString();
                if (uuidToFile.ContainsKey(uuid))
                {
                    var fullName2 = uuidToFile[uuid];
                    if (!mapDfs.Contains(fullName2))
                    {
                        dfs(fullName2);
                    }
                    fullName2 = fullName2 + ".meta";
                    if (!mapDfs.Contains(fullName2))
                    {
                        dfs(fullName2);
                    }
                }
            }
        }
    }
}