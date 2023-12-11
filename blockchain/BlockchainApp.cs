using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace BlockchainAssignment
{
    public partial class BlockchainApp : Form
    {
        Blockchain blockchain;
        bool enableAutominer = false;
        bool enableAPOW = true;
        float tarBlockTime = 10;
        int sleepTimer = 500;
        int threadNum = 2;
        int difficulty = 5;

        public BlockchainApp()
        {
            InitializeComponent();
            blockchain = new Blockchain();
            richTextBox1.Text = "New Blockchain Initialised!";
        }

        
        private void button1_Click_1(object sender, EventArgs e)
        {
            richTextBox1.Text=textBox1.Text;
            try
            {
                setRTB1Text(blockchain.GetBlockOutput(Int32.Parse(textBox1.Text)));
            }
            catch (FormatException)
            {
                setRTB1Text("Invalid Input");
            }
        }

        private void setRTB1Text(string str)
        {
            if (InvokeRequired)
            {
                this.Invoke(new Action<string>(setRTB1Text), new object[] {
          str
        });
                return;
            }
            richTextBox1.Text = str;
        }
        private void setAPoWText(string str)
        {
            if (InvokeRequired)
            {
                this.Invoke(new Action<string>(setAPoWText), new object[] {
          str
        });
                return;
            }
            aPow.Text = str;
        }
        private void button2_Click_1(object sender, EventArgs e)
        {
            String privKey, pubKey;
            Wallet.Wallet wallet = new Wallet.Wallet(out privKey);
            pubKey = wallet.publicID;
            txtPubKey.Text = pubKey;
            txtPrivKey.Text = privKey;
            setRTB1Text("Created new Wallet");
        }
        private void button3_Click(object sender, EventArgs e)
        {
            if (Wallet.Wallet.ValidatePrivateKey(txtPrivKey.Text, txtPubKey.Text))
            {
                setRTB1Text("Keys are Valid");
            }
            else
            {
                setRTB1Text("Keys are INVALID");
            }
        }
        private void button4_Click(object sender, EventArgs e)
        {
            double walletBalance = blockchain.GetBalance(txtPubKey.Text);
            if (walletBalance < float.Parse(txtAmnt.Text))
            {
                setRTB1Text("ERROR: Too low balance to make transaction");
                return;
            }
            if (!Wallet.Wallet.ValidatePrivateKey(txtPrivKey.Text, txtPubKey.Text))
            {
                setRTB1Text("ERROR: Keys provided were invalid");
                return;
            }
            Transaction trans = new Transaction(txtPubKey.Text, txtPrivKey.Text, txtRKey.Text, float.Parse(txtAmnt.Text), float.Parse(txtFee.Text));
            setRTB1Text(trans.ReturnInfo());
            blockchain.transactionPool.Add(trans);
        }
        private void button5_Click(object sender, EventArgs e)
        {
            if (!Wallet.Wallet.ValidatePrivateKey(txtPrivKey.Text, txtPubKey.Text))
            {
                setRTB1Text("ERROR: Can't Mine blocks with invalid Keys");
                return;
            }
            Task mine = Task.Run(() => {
                Miner(txtPubKey.Text, false);
            });
        }
        private void button6_Click(object sender, EventArgs e)
        {
            string blockchainInfo = blockchain.ReturnInfo();
            setRTB1Text(blockchainInfo);
        }
        private void button7_Click(object sender, EventArgs e)
        {
            string transPoolInfo = blockchain.ReturnTransPoolInfo();
            if (transPoolInfo == String.Empty)
            {
                transPoolInfo = "No more pending transactions in the pool";
            }
            setRTB1Text(transPoolInfo);
        }
        private void button9_Click(object sender, EventArgs e)
        {
            setRTB1Text(blockchain.GetBalance(txtPubKey.Text).ToString() + " AssignmentCoin");
        }
        private void button10_Click(object sender, EventArgs e)
        {
            if (blockchain.Blocks.Count == 1)
            {
                if (blockchain.ValidateMerkelRoot(blockchain.Blocks[0])) 
                {
                    setRTB1Text("Valid Blockchain"); 
                }
                else
                {
                    setRTB1Text("Invalid Blockchain: Merkleroot"); 
                }
                return;
            }
            else
            {
                for (int i = 1; i < blockchain.Blocks.Count; i++) 
                {
                    if (
                      blockchain.Blocks[i].previousHash != blockchain.Blocks[i - 1].Hash || 
                      !blockchain.ValidateMerkelRoot(blockchain.Blocks[i]) || 
                      !blockchain.ValidateHash(blockchain.Blocks[i]) 
                    )
                    {
                        setRTB1Text("Invalid Hash History in Block " + i.ToString()); 
                        return;
                    }
                    if (!blockchain.ValidateTransactions(blockchain.Blocks[i])) 
                    {
                        setRTB1Text("Invalid Blockchain: Invalid Transaction in Block " + i.ToString()); 
                        return;
                    }
                }
            }
            setRTB1Text("Valid Blockchain"); 
        }
        private void button8_Click(object sender, EventArgs e)
        {
            if (!Wallet.Wallet.ValidatePrivateKey(txtPrivKey.Text, txtPubKey.Text))
            {
                setRTB1Text("ERROR: Can't Mine blocks with invalid Keys");
                return;
            }
            Task mine = Task.Run(() => {
                Miner(txtPubKey.Text, true);
            });
        }

        private void button11_Click(object sender, EventArgs e)
        {
            this.enableAutominer = true;
            Task ts = Task.Run(() => {
                while (enableAutominer)
                {
                    Miner("AUTOMINER", true);
                }
            });
        }
        private void Miner(String recieverAddress, bool threaded)
        {
            Thread.Sleep(this.sleepTimer);
            int comboInput = 1;
            String comboSetting = String.Empty;
            this.Invoke((MethodInvoker)delegate () {
                comboInput = cmbo_MineMethod.SelectedIndex;
                comboSetting = cmbo_MineMethod.SelectedItem.ToString();
            });
            int numOfTrans = 3;
            String str = String.Empty;
            int transPoolCount = blockchain.transactionPool.Count();
            if (transPoolCount < numOfTrans)
            {
                str += "WARNING: Only " + transPoolCount + " transactions being added to block!\n";
                numOfTrans = transPoolCount;
            }
            Console.WriteLine("Transaction Selection Setting: " + comboSetting);
            List<Transaction> blockTransactions = blockchain.GetTransactionList(comboInput, numOfTrans, txtPubKey.Text);
            blockchain.transactionPool = blockchain.transactionPool.Except(blockTransactions).ToList();
            Block newBlock = new Block(blockchain.GetLastBlock(), blockTransactions, recieverAddress, threaded, this.difficulty, this.threadNum);
            blockchain.Blocks.Add(newBlock);
            str += "\n" + newBlock.ReturnInfo();

            setRTB1Text(str);
        }
        private void BlockchainApp_Load(object sender, EventArgs e)
        {
            cmbo_MineMethod.SelectedIndex = 0;

            this.txtMineTime.Enabled = false;
        }

        private void button12_Click(object sender, EventArgs e)
        {
            this.enableAutominer = false;
        }
        private void button13_Click(object sender, EventArgs e)
        {
            this.txtMineTime.Enabled = true;
            Task ts = Task.Run(() => {
                while (enableAPOW)
                {
                    List<DateTime> recentTimes = new List<DateTime>();
                    List<int> diffSeconds = new List<int>();
                    double averageSeconds = 0;
                    String str = "";
                    for (int i = 0; i < 10; i++)
                    {
                        try
                        {
                            recentTimes.Add(blockchain.Blocks[blockchain.Blocks.Count - 1 - i].timestamp);
                        }
                        catch (ArgumentOutOfRangeException)
                        {
                            break;
                        }
                    }
                    if (recentTimes.Count <= 1)
                    {
                        str += "Not enough Blocks";
                    }
                    else
                    {
                        str += "Actual Block Time: ";
                        for (int i = 0; i < recentTimes.Count - 1; i++)
                        {
                            diffSeconds.Add((int)(recentTimes[i] - recentTimes[i + 1]).TotalSeconds);
                        }
                        averageSeconds = diffSeconds.Average();
                        str += averageSeconds.ToString("n2");
                    }
                    str += "\nTarget Block time: " + this.tarBlockTime.ToString("n2");
                    adaptDifficulty(averageSeconds);
                    str += "\nDifficulty : " + this.difficulty.ToString();
                    str += "\nArtificial Sleep (ms): " + this.sleepTimer.ToString();
                    setAPoWText(str);
                    Thread.Sleep(1000);
                }
            });
        }
        private void adaptDifficulty(double CurrentBlockTime)
        {
            float t = this.tarBlockTime;
            if (t < 0.5)
            {
                this.difficulty = 3;
            }
            else if (t >= 0.5 && t < 9.5)
            {
                this.difficulty = 4;
            }
            else if (t >= 9.5 && t < 200)
            {
                this.difficulty = 5;
            }
            else if (t >= 200)
            {
                this.difficulty = 6;
            }
            this.sleepTimer = (int)((t - CurrentBlockTime) * 1000);
            if (this.sleepTimer < 0)
            {
                this.sleepTimer = 0;
                if (CurrentBlockTime / t > 1.5)
                {
                    this.difficulty--;
                }
            }
        }
        private void button14_Click(object sender, EventArgs e)
        {
            this.enableAPOW = false;
            this.sleepTimer = 0;
            this.txtMineTime.Enabled = false;
            setAPoWText("Disabled");
        }
        private void txtMineTime_TextChanged(object sender, EventArgs e)
        {
            try
            {
                this.tarBlockTime = float.Parse(txtMineTime.Text);
                txtMineTime.BackColor = Color.Green;
            }
            catch (FormatException)
            {
                this.tarBlockTime = 30;
                txtMineTime.BackColor = Color.Red;
                return;
            }
        }

    
        private void button15_Click(object sender, EventArgs e)
        {
            String privKey = "PjshII779n;n89JJpkLU@UE+AUtMaW1b$RVoUf1\"jaiq8Uuwh28/'sl?lqp-x";
            String pubKey = ".<>I`ZW(L:'jw2810mBUm2m740Nla;\|i92,>u229,q22Hkwmn9*nw9I)wi2mBBol";
            Random rnd = new Random();
            for (int i = 0; i < 10; i++)
            {
                float amount = (float)(rnd.NextDouble() * 1000);
                float fee = (float)(rnd.NextDouble() * 100);
                Transaction trans = new Transaction(pubKey, privKey, "TEST", amount, fee);
                Thread.Sleep((int)(rnd.NextDouble() * 10000));
                blockchain.transactionPool.Add(trans);
            }
        }

        private void richTextBox1_TextChanged(object sender, EventArgs e)
        {

        }
    }
}