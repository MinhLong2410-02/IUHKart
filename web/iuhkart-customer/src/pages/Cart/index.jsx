import { useCallback, useEffect, useMemo, useState } from "react";
import {
  Box,
  Button,
  Divider,
  Flex,
  Heading,
  Image,
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
  const [cart, setCart] = useState({});

  useEffect(() => {
    const getCartProducts = async () => {
      const data = await cartAPI.getCartProducts();

      setCart(data);
      setLoading(false);
    };

    getCartProducts();
  }, [setCart]);

  const handleRemoveProduct = useCallback(
    async (productID) => {
      console.log(productID);

      try {
        const data = await cartAPI.deleteProductFromCart(productID);

        setCart(data);

        toast({
          title: "Remove Product From Cart Successful!",
          status: "success",
          position: "top-right",
        });
      } catch (error) {
        toast({
          title: "Remove Product From Cart Fail!",
          status: "error",
          position: "top-right",
        });
      }
    },
    [toast]
  );

  const renderListCartItem = useMemo(() => {
    return (
      <Stack>
        {!_.isEmpty(cart) &&
          cart?.products?.map((product, index) => {
            const productImage =
              product?.product?.["main_image"]?.["image_url"];
            const productName = product?.product?.["product_name"];
            const productPrice = product?.product?.["original_price"];

            return (
              <Flex key={index} borderY="1px solid #e9e9e9">
                <Box boxSize="sm">
                  <Image src={productImage} />
                </Box>
                <Stack flex={1} justifyContent="center">
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
                      handleRemoveProduct(product?.product?.["product_id"])
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
  }, [cart, handleRemoveProduct]);

  return (
    <Box paddingX="5%" paddingY="20px">
      {isLoading ? (
        <Flex justifyContent="center">
          <Spinner size="xl" color="#3734a9" />
        </Flex>
      ) : (
        <>
          <Box marginY="15px">
            <Heading>Shopping cart</Heading>
          </Box>
          <Flex>
            {renderListCartItem}
            {!!cart["items_total"] && (
              <Box>
                <Box marginX="40px" padding="20px" backgroundColor="#f5f5f7">
                  <Box marginBottom="15px">
                    <Box marginBottom="20px">
                      <Text whiteSpace="nowrap" fontSize="2xl">
                        Order details
                      </Text>
                    </Box>
                    <Box>
                      <Flex gap={10} justifyContent="space-between">
                        <Text whiteSpace="nowrap">{`Subtotal (${cart["items_total"]} items)`}</Text>
                        <Text whiteSpace="nowrap">{`${cart["grand_total"]} VND`}</Text>
                      </Flex>
                    </Box>
                    <Divider marginY="10px" orientation="horizontal" />
                    <Box>
                      <Flex gap={10} justifyContent="space-between">
                        <Text whiteSpace="nowrap" fontWeight={600}>
                          Grand Total
                        </Text>
                        <Text
                          whiteSpace="nowrap"
                          fontWeight={600}
                        >{`${cart["grand_total"]} VND`}</Text>
                      </Flex>
                    </Box>
                  </Box>
                  <Box>
                    <Button
                      width="100%"
                      size="lg"
                      backgroundColor="#3734a9"
                      color="white"
                      _hover={{
                        backgroundColor: "#333190",
                      }}
                    >
                      Proceed payment
                    </Button>
                  </Box>
                </Box>
              </Box>
            )}
          </Flex>
        </>
      )}
    </Box>
  );
};

export default Cart;
