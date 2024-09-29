import { Box, Flex, Heading, Stack } from "@chakra-ui/react";

import FilterModule from "../../modules/FilterModule";
import ProductGrid from "../../modules/ProductGrid";
import { ProductProvider } from "../../contexts/ProductContext";

const Home = () => {
  return (
    <Stack>
      {/* <Box
        height="100vh"
        backgroundImage={`linear-gradient(to right, #c7e6f2, #a5d8ea, #94d0e6, #6dbfdd)`}
        backgroundBlendMode="multiply"
      ></Box> */}
      <Stack paddingX="5%">
        <Box>
          <Box marginY="50px" textAlign="center">
            <Heading as="h3" size="2xl">
              Our featured store
            </Heading>
          </Box>
          <ProductProvider>
            <Flex gap={5}>
              <FilterModule />
              <ProductGrid />
            </Flex>
          </ProductProvider>
        </Box>
      </Stack>
    </Stack>
  );
};

export default Home;
