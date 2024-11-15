import {
  Box,
  Flex,
  Heading,
  IconButton,
  Image,
  Stack,
  Text,
} from "@chakra-ui/react";
import { Icon } from "@iconify/react/dist/iconify.js";

import sampleImage from "../../assets/images/sample.jpg";

const ProductCard = ({ product, onAddCart, onClick }) => {
  return (
    <Box
      position="relative"
      padding="8px"
      borderRadius="12px"
      boxShadow="rgba(99, 99, 99, 0.2) 0px 2px 8px 0px"
      _hover={{ cursor: "pointer" }}
    >
      <Stack onClick={() => onClick(product)}>
        <Box borderRadius="10px" overflow="hidden">
          <Image
            src={product?.images ? product?.images?.image_url : sampleImage}
            width="100%"
            aspectRatio={1}
            objectFit="cover"
          />
        </Box>

        <Box>
          <Heading as="h4" size="sm" noOfLines={2}>
            {product?.product_name}
          </Heading>
        </Box>

        <Flex gap={3}>
          <Text>
            Brand: <Text as="b">{product.brand}</Text>
          </Text>
        </Flex>

        <Text as="b">{`${product?.original_price} VND`}</Text>
      </Stack>
      <Box position="absolute" right="8px" bottom="8px">
        <IconButton
          size="lg"
          icon={<Icon icon="vaadin:cart-o" />}
          textColor="white"
          borderRadius="20px"
          backgroundColor="#3734a9"
          _hover={{
            backgroundColor: "#333190",
          }}
          onClick={(e) => {
            e.preventDefault();
            onAddCart(product["product_id"]);
          }}
        />
      </Box>
    </Box>
  );
};

export default ProductCard;
