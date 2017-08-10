using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace pitch_2
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            comboBox1.Items.Add("1");
            comboBox1.Items.Add("2");
            comboBox1.Items.Add("3");
            comboBox1.Items.Add("4");
            comboBox1.Items.Add("5");
            comboBox1.Items.Add("6");
            comboBox1.Items.Add("7");
            comboBox1.SelectedIndex = 0;
            radioButton1.Checked = true;
            radioButton3.Checked = true;
            textBox1.Text = "1";
        }
        private void button1_Click(object sender, EventArgs e)
        {
            label4.Text = "";
            try
            {
                start();
            }
            catch (Exception err)
            {

                MessageBox.Show(err.Message);
            }
        }
        private string getfilename()
        {
            string currentdir = Environment.CurrentDirectory;
            FileInfo[] files ;
            if (radioButton1.Checked)
            {
                files = new DirectoryInfo(currentdir).GetFiles("*.rtl");
            }
            else
            {
                files = new DirectoryInfo(currentdir).GetFiles("*.rta");
            }
            if (files.LongCount()==0)
            {
                throw new Exception("测量文件不存在");
            }
            else
            {
                return files[0].ToString();
            }
        }
        private List<string> readfile(string filename)
        {
            List<string> txt=File.ReadAllLines(filename).ToList();
            List<string> pointlines = new List<string> { };
            int state = 0;
            foreach (string line in txt)
            {
             
                if (state == 1)
                {
                    pointlines.Add(line);
                }
                if (line == "Run Target Data: " || line == "Run Target Data:")
                {
                    state = 1;
                }
                if (line == "EQUIPMENT::" || line == "ENVIRONMENT::")
                {
                    state = 0;
                }
            }
            try
            {
                pointlines.RemoveRange(pointlines.IndexOf("EQUIPMENT::") - 1, 2);

            }
            catch (Exception)
            {
                pointlines.RemoveRange(pointlines.IndexOf("ENVIRONMENT::") - 1, 2);
            }
            return pointlines;
        }
        private List<float> getpoints(List<string> pointlines,int direct)
        {
            List<float> points = new List<float> { };
            foreach (string line in pointlines)
            {
                List<string> line1 = new List<string> { };
                foreach (string i in line.Split(' '))
                {
                    if (i!="")
                    {                       
                        line1.Add(i);
                    }
                }
                if (line1[0]=="1")
                {
                    points.Add(float.Parse(line1[2]));
                }
                else
                {
                    points[int.Parse(line1[1]) - 1] += float.Parse(line1[2]);                
                }
            }
            if (direct==1)
            {
                List<float> points1 = new List<float> { };
                for (int i = (int)points.LongCount()-1; i >=0; i--)
                {
                    points1.Add(points[i]);
                }
                return points1;
            }
            else
            {
                return points;
            }
        }
        private List<int> calculate(List<float> points, int measureTimes,float k,float mini,int times)
        {
            for (int i = 1; i < points.LongCount(); i++)
            {
                points[i] = (points[i] - points[0]) * k / measureTimes;               
            }
            points[0] = 0;
            List<int> results = new List<int> { };
            results.Add(0);
            for (int i = 1; i < points.LongCount(); i++)
            {
                int sum=0;
                for (int j = 0; j < i; j++)
                {
                    sum += results[j];
                }
                results.Add((int)Math.Round(-(points[i] + sum * times * mini)/mini/times));
            }
            return results;
        }
        private void print(int  rank,List<int>   results)
        {
            listBox1.Items.Clear();
            for (int i = 0; i < results.LongCount(); i++)
            {
                listBox1.Items.Add((rank + i).ToString() + " : " + results[i].ToString());
            }
        }
        private void start()
        {
            int direct = 0;
            float mini = 1;
            float k = 1;
            int measureTimes;
            int rank;
            try
            {
                rank = int.Parse(textBox2.Text);
            }
            catch (Exception)
            {

                throw new Exception("起始序号输入无效");
            }
            try
            {
                measureTimes = int.Parse(textBox1.Text);
            }
            catch (Exception)
            {

                throw new Exception("测量次数输入无效");
            }
            if (measureTimes == 0)
            {
                throw new Exception("测量次数输入无效");
            }
            if (radioButton4.Checked)
            {
                direct = 1;
            }
            int times = comboBox1.SelectedIndex + 1;
            if (times > 7 || times < 1)
            {
                throw new Exception("倍率选择错误");
            }
            if (radioButton2.Checked)
            {
                k = 206.264f;
                mini = 3.6f;
            }
            List<float> points = getpoints(readfile(getfilename()), direct);
            List<int> results = calculate(points, measureTimes, k, mini, times);
            print(rank, results);
            if (radioButton2.Checked)
            {
                int sum = 0;
                foreach (int i in results)
                {
                    sum += i;
                }
                if (sum!=0)
                {
                    label4.Text =string.Format("补偿值合为{0}",sum);
                }
            }
        }
    }
    
}
