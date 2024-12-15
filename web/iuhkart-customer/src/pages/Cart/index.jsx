import { useCallback, useEffect, useMemo, useState } from "react";
import {
  Box,
  Button,
  Divider,
  Flex,
  Heading,
  Image,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  NumberDecrementStepper,
  NumberIncrementStepper,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  Spinner,
  Stack,
  Text,
  useToast,
} from "@chakra-ui/react";
import _ from "lodash";

import cartAPI from "../../api/cart.api";

const Cart = () => {
  const toast = useToast();

  const [isLoading, setLoading] = useState(true);
  const [cart, setCart] = useState({ products: [], items_total: 0, grand_total: 0 });
  const [isOpenModal, setIsOpenModal] = useState(false);
  const [dataModal, setDataModal] = useState([]);

  console.log(cart.products);

  // Fetch cart products
  useEffect(() => {
    const getCartProducts = async () => {
      try {
        const data = await cartAPI.getCartProducts();
        setCart(data || { products: [], items_total: 0, grand_total: 0 });
      } catch (error) {
        toast({
          title: "Failed to load cart products.",
          status: "error",
          position: "top-right",
        });
      } finally {
        setLoading(false);
      }
    };

    getCartProducts();
  }, [toast]);

  // Remove product from cart
  const handleRemoveProduct = useCallback(
    async (productID) => {
      try {
        const data = await cartAPI.deleteProductFromCart(productID);
        setCart(data);

        toast({
          title: "Product removed from cart successfully!",
          status: "success",
          position: "top-left",
        });
      } catch (error) {
        toast({
          title: "Failed to remove product from cart.",
          status: "error",
          position: "top-left",
        });
      }
    },
    [toast]
  );

  // Proceed to payment
  const handleClickProceedPayment = useCallback(() => {
    const getOrder = async () => {
      try {
        const data = await cartAPI.createOrder(
          {
            "products": cart.products.map((product) => ({
              "product_id": product.product.product_id,
              "quantity": product.quantity,
            })),
          }
        );
        setDataModal(data);
      } catch (error) {
        toast({
          title: "Failed to create order.",
          status: "error",
          position: "top-right",
        });
      }
    }

    getOrder();
    setIsOpenModal(true);
  }, [cart]);



  // Confirm payment
  const handleConfirmPayment = useCallback(() => {
    const confirmPayment = async () => {
      try {
        await cartAPI.confirmOrder({
          "order_ids": dataModal.map((order) => order.order_id),
        });
        toast({
          title: "Payment successful!",
          status: "success",
          position: "top-right",
        });
        setIsOpenModal(false);
      } catch (error) {
        toast({
          title: "Failed to confirm payment.",
          status: "error",
          position: "top-right",
        });
      }
    }
    confirmPayment();
  });


  // Render list of cart items
  const renderListCartItem = useMemo(() => {
    if (_.isEmpty(cart.products)) {
      return <Text>No products in the cart.</Text>;
    }

    return (
      <Stack>
        {cart.products.map((product, index) => {
          const productImage = product?.product?.main_image?.image_url;
          const productName = product?.product?.product_name;
          const productPrice = product?.product?.original_price;

          return (
            <Flex key={index} borderY="1px solid #e9e9e9" paddingY={4}>
              <Box boxSize="sm">
                <Image src={productImage} alt={productName} />
              </Box>
              <Stack flex={1} justifyContent="center" paddingLeft={4}>
                <Heading as="h4" size="md" noOfLines={2}>
                  {productName}
                </Heading>
                <Text fontSize="lg">{`${productPrice} VND`}</Text>
              </Stack>
              <Stack justifyContent="center" paddingX={2}>
                <NumberInput defaultValue={product?.quantity} min={1}>
                  <NumberInputField />
                  <NumberInputStepper>
                    <NumberIncrementStepper />
                    <NumberDecrementStepper />
                  </NumberInputStepper>
                </NumberInput>
              </Stack>
              <Stack justifyContent="center" paddingX={2}>
                <Button
                  variant="outline"
                  onClick={() =>
                    handleRemoveProduct(product?.product?.product_id)
                  }
                >
                  Remove
                </Button>
              </Stack>
            </Flex>
          );
        })}
      </Stack>
    );
  }, [cart.products, handleRemoveProduct]);

  return (
    <Box paddingX="5%" paddingY="20px">
      {isLoading ? (
        <Flex justifyContent="center">
          <Spinner size="xl" color="#3734a9" />
        </Flex>
      ) : (
        <>
          <Box marginY="15px">
            <Heading>Shopping Cart</Heading>
          </Box>
          <Flex>
            {renderListCartItem}
            {cart.items_total > 0 && (
              <Box>
                <Box marginX="40px" padding="20px" backgroundColor="#f5f5f7">
                  <Box marginBottom="15px">
                    <Box marginBottom="20px">
                      <Text whiteSpace="nowrap" fontSize="2xl">
                        Order Details
                      </Text>
                    </Box>
                    <Box>
                      <Flex gap={10} justifyContent="space-between">
                        <Text whiteSpace="nowrap">{`Subtotal (${cart.items_total} items)`}</Text>
                        <Text whiteSpace="nowrap">{`${cart.grand_total} VND`}</Text>
                      </Flex>
                    </Box>
                    <Divider marginY="10px" orientation="horizontal" />
                    <Box>
                      <Flex gap={10} justifyContent="space-between">
                        <Text whiteSpace="nowrap" fontWeight={600}>
                          Grand Total
                        </Text>
                        <Text whiteSpace="nowrap" fontWeight={600}>
                          {`${cart.grand_total} VND`}
                        </Text>
                      </Flex>
                    </Box>
                  </Box>
                  <Box>
                    <Button
                      width="100%"
                      size="lg"
                      backgroundColor="#3734a9"
                      color="white"
                      _hover={{ backgroundColor: "#333190" }}
                      onClick={handleClickProceedPayment}
                    >
                      Proceed Payment
                    </Button>
                  </Box>
                </Box>
              </Box>
            )}
          </Flex>

          <Modal isOpen={isOpenModal} onClose={() => setIsOpenModal(false)}>
            <ModalOverlay />
            <ModalContent>
              <ModalHeader>Payment</ModalHeader>
              <ModalBody>
                {dataModal?.map((order, index) => (
                  <Box key={index} padding="10px" borderBottom="1px solid #e9e9e9">
                    <Text fontWeight="bold" marginBottom="5px">{`Order ID: ${order.order_id}`}</Text>
                    <Text marginBottom="10px">{`Total: ${order.order_total.toLocaleString()} VND`}</Text>
                    <Text fontWeight="semibold" marginBottom="5px">Products:</Text>
                    <Stack spacing={3}>
                      {order.products.map((product, productIndex) => (
                        <Flex key={productIndex} alignItems="center" gap="10px">
                          <Image
                            src={product.image_url}
                            alt={product.product_name}
                            boxSize="50px"
                            objectFit="cover"
                          />
                          <Box>
                            <Text>{product.product_name}</Text>
                            <Text>{`Price: ${product.price.toLocaleString()} VND`}</Text>
                            <Text>{`Quantity: ${product.quantity}`}</Text>
                          </Box>
                        </Flex>
                      ))}
                    </Stack>
                  </Box>
                ))}
              </ModalBody>
              <ModalFooter>
                <Button
                  backgroundColor="#3734a9"
                  color="white"
                  _hover={{ backgroundColor: "#333190" }}
                  onClick={handleConfirmPayment}
                >
                  Confirm Payment
                </Button>
              </ModalFooter>
            </ModalContent>
          </Modal>

        </>
      )}
    </Box>
  );
};

export default Cart;
