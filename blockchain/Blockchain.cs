using System;
using System.Collections.Generic;
using System.Linq;


namespace BlockchainAssignment
{
    class Blockchain
    {
        public List<Block> Blocks = new List<Block>();
        public List<Transaction> transactionPool = new List<Transaction>();
        public Blockchain()
        {
            Blocks.Add(new Block());
        }
        public List<Transaction> GetTransactionList(int mode, int no_of_trans, String minerAddress)
        {
            List<Transaction> returnList = new List<Transaction>();
            if (no_of_trans == transactionPool.Count)
            {
                return transactionPool;
            }
            else
            {
              
                if (mode == 0)
                {
                    returnList = transactionPool.OrderBy(t => t.fee)
                      .Reverse()
                      .ToList();
                    returnList.RemoveRange(no_of_trans, returnList.Count - (no_of_trans));
                }
                else if (mode == 1)
                {
                    var random = new Random();
                    List<Transaction> tempList = transactionPool.ToList();
                    for (int i = 0; i < no_of_trans; i++)
                    {
                        int rndIndex = random.Next(0, tempList.Count);
                        returnList.Add(tempList[rndIndex]);
                        tempList.RemoveAt(rndIndex);
                    }
                }
                else if (mode == 2)
                {
                    returnList = transactionPool.OrderBy(t => t.timestamp)
                      .ToList();
                    returnList.RemoveRange(no_of_trans, returnList.Count - (no_of_trans));
                }

                else if (mode == 3)
                {
                    foreach (Transaction t in transactionPool)
                    {
                        if (t.RecipientAddress.Equals(minerAddress) || t.SenderAddress.Equals(minerAddress))
                        {
                            returnList.Add(t);
                        }
                        if (returnList.Count == no_of_trans)
                        {
                            break;
                        }
                    }
                }

                if (returnList.Count != no_of_trans)
                {
                    List<Transaction> resultList = transactionPool.Except(returnList).ToList();
                    for (int i = 0; i < (no_of_trans - returnList.Count); i++)
                    {
                        returnList.Add(resultList[i]);
                    }
                }

            }
            foreach (Transaction t in returnList)
            {
                Console.WriteLine("\nAmount: " + t.amount.ToString() +
                  "\nFee: " + t.fee.ToString() +
                  "\nTimestamp: " + t.timestamp.ToString() +
                  "\nSender: " + t.SenderAddress +
                  "\nRecipient: " + t.RecipientAddress);
            }
            return returnList;
        }
        public String GetBlockOutput(int blockIndex)
        {
            try
            {
                return Blocks[blockIndex].ReturnInfo();
            }
            catch (ArgumentOutOfRangeException)
            {
                return "Block doesn't exist";
            }
        }
        public Block GetLastBlock()
        {
            return Blocks[Blocks.Count - 1];
        }
        public String ReturnInfo()
        {
            string str = String.Empty;
            foreach (Block curBlock in Blocks)
            {
                str += curBlock.ReturnInfo();
                str += "\n\n";
            }
            return str;
        }
        public bool ValidateHash(Block b)
        {
            String rehash = b.CreateHash();
            Console.WriteLine("Validate Hash: " + rehash.Equals(b.Hash).ToString());
            return rehash.Equals(b.Hash);
        }

        public bool ValidateMerkelRoot(Block b)
        {
            String reMerkle = Block.MerkleRoot(b.transactionList);
            Console.WriteLine("Validate MerkleRoot: " + reMerkle.Equals(b.merkleRoot).ToString());
            return reMerkle.Equals(b.merkleRoot);
        }

  
        public bool ValidateTransactions(Block b)
        {
            foreach (Transaction t in b.transactionList)
            {
                if (t.Signature == "null" || !Wallet.Wallet.ValidateSignature(t.SenderAddress, t.Hash, t.Signature))
                {
                    return false;
                }
            }
            return true;
        }

        public double GetBalance(String address)
        {
            double balance = 0;
            foreach (Block b in Blocks)
            {
                foreach (Transaction t in b.transactionList)
                {
                    if (t.RecipientAddress.Equals(address))
                    {
                        balance += t.amount;
                    }
                    if (t.SenderAddress.Equals(address))
                    {
                        balance -= (t.amount + t.fee);
                    }
                }
            }
            foreach (Transaction t in this.transactionPool)
            {
                if (t.RecipientAddress.Equals(address))
                {
                    balance += t.amount;
                }
                if (t.SenderAddress.Equals(address))
                {
                    balance -= (t.amount + t.fee);
                }
            }
            return balance;
        }

        public String ReturnTransPoolInfo()
        {
            string str = String.Empty;
            foreach (Transaction t in transactionPool)
            {
                str += "\n\nIndex:" + transactionPool.IndexOf(t) + "\n" + t.ReturnInfo();
            }
            if (str == String.Empty)
            {
                str += "No Pending Transactions";
            }
            return str;
        }

    }
}