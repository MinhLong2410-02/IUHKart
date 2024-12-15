import { Box, Button, Flex, Heading, Input, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, SimpleGrid, Spinner, Text, useDisclosure, useToast } from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import walletAPI from '../../api/wallet.api';

const Wallet = () => {
  const [wallet, setWallet] = useState(null);
  const [isLoading, setLoading] = useState(true);
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [amount, setAmount] = useState('');
  const toast = useToast();

  useEffect(() => {
    const fetchWalletDetails = async () => {
      const data = await walletAPI.getWalletDetails();
      setWallet(data);
      setLoading(false);
    };

    fetchWalletDetails();
  }, []);

  const handleAddMoney = async () => {
    try {
      const data = await walletAPI.addMoneyToWallet({money: amount });
      setWallet(data);
      toast({
        title: "Money added successfully!",
        status: "success",
        position: "top-right",
      });

      onClose();
    } catch (error) {
        console.log(error);
      toast({
        title: "Failed to add money!",
        status: "error",
        position: "top-right",
      });
    } finally{
        const data = await walletAPI.getWalletDetails();
        setWallet(data);
    }
  };

  if (isLoading) {
    return (
      <Flex justifyContent="center" alignItems="center" height="100vh">
        <Spinner size="xl" color="#3734a9" />
      </Flex>
    );
  }

  return (
    <Box padding="5%">
      <Heading as="h2" size="xl" marginBottom="20px">
        Wallet Details
      </Heading>
      <SimpleGrid columns={{ base: 1, md: 2 }} spacing={10}>
        <Box borderWidth="1px" borderRadius="lg" padding="20px">
          <Text fontSize="lg"><strong>Bank Name:</strong> {wallet.bank_name}</Text>
        </Box>
        <Box borderWidth="1px" borderRadius="lg" padding="20px">
          <Text fontSize="lg"><strong>Account Number:</strong> {wallet.account_number}</Text>
        </Box>
        <Box borderWidth="1px" borderRadius="lg" padding="20px">
          <Text fontSize="lg"><strong>Account Holder Name:</strong> {wallet.account_holder_name}</Text>
        </Box>
        <Box borderWidth="1px" borderRadius="lg" padding="20px">
          <Text fontSize="lg"><strong>Current Balance:</strong> {wallet.current_balance} VND</Text>
        </Box>
      </SimpleGrid>
      <Button marginTop="20px" colorScheme="blue" onClick={onOpen}>
        Add Money
      </Button>

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Add Money to Wallet</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Input
              placeholder="Enter amount"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              type="number"
            />
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="blue" mr={3} onClick={handleAddMoney}>
              Add
            </Button>
            <Button variant="ghost" onClick={onClose}>Cancel</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Box>
  );
};

export default Wallet;