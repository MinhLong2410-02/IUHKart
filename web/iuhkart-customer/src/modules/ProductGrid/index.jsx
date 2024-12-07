import { useCallback, useContext, useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Flex,
  Grid,
  GridItem,
  Heading,
  Select,
  Spinner,
  Stack,
  Text,
  useToast,
} from "@chakra-ui/react";
import _ from "lodash";

import productApi from "../../api/product.api";
import cartAPI from "../../api/cart.api";

import { GlobalContext } from "../../contexts/GlobalContext";
import { ProductContext } from "../../contexts/ProductContext";

import ProductCard from "../../components/ProductCard";
import Pagination from "../../components/Pagination";

import { PRODUCT_PAGING } from "./constants";

const ProductGrid = () => {
  const navigate = useNavigate();
  const toast = useToast();

  const { setProductID } = useContext(GlobalContext);
  const { categorySelected } = useContext(ProductContext);

  const [isLoading, setLoading] = useState(false);
  const [productDataSet, setProductDataSet] = useState({});
  const [pageCount, setPageCount] = useState(0);

  useEffect(() => {
    const getProducts = async () => {
      setLoading(true);

      const data = await productApi.getProducts(
        categorySelected,
        1,
        PRODUCT_PAGING.pageSize
      );
      const dataCount = data?.count || 0;
      setLoading(false);
      setProductDataSet(data);
      setPageCount(Math.ceil(dataCount / PRODUCT_PAGING.pageSize));
    };

    getProducts();
  }, [categorySelected, setProductDataSet, setPageCount]);

  const handlePageClick = async (data) => {
    setLoading(true);

    const pageSelected = data?.selected + 1;
    const dataProduct = await productApi.getProducts(
      pageSelected,
      PRODUCT_PAGING.pageSize
    );

    setLoading(false);
    setProductDataSet(dataProduct);
  };

  const handleClickProduct = useCallback(
    (product) => {
      setProductID(product["product_id"]);
      navigate(`/products/${product["product_id"]}`);
    },
    [navigate, setProductID]
  );

  const handleAddCart = useCallback(
    async (productID) => {
      try {
        const payload = {
          product: productID,
          quantity: 1,
        };

        const data = await cartAPI.addProduct(payload);

        if (!_.isEmpty(data))
          toast({
            title: "Add Cart Successful!",
            status: "success",
            position: "top-right",
          });
      } catch (error) {
        toast({
          title: "Add Cart Fail!",
          status: "error",
          position: "top-right",
        });
      }
    },
    [toast]
  );

  const renderGridProduct = useMemo(() => {
    const listProduct = productDataSet?.results || [];
    return (
      <>
        {isLoading ? (
          <Flex justifyContent="center">
            <Spinner size="xl" color="#3734a9" />
          </Flex>
        ) : (
          <Grid templateColumns="repeat(4, 1fr)" gap={5}>
            {!_.isEmpty(listProduct) &&
              listProduct.map((product, index) => (
                <GridItem
                  key={index}
                  // onClick={() => handleClickProduct(product)}
                >
                  <ProductCard
                    product={product}
                    onAddCart={handleAddCart}
                    onClick={handleClickProduct}
                  />
                </GridItem>
              ))}
          </Grid>
        )}
      </>
    );
  }, [isLoading, productDataSet, handleClickProduct, handleAddCart]);

  return (
    <Stack flex={1}>
      <Flex marginBottom="15px" justifyContent="space-between">
        <Flex alignItems="center" gap={3}>
          <Heading as="h3" size="lg">
            Ankara styles
          </Heading>
          <Text>Male & Female</Text>
        </Flex>
        <Box>
          <Select placeholder="Select option">
            <option value="popular">Popular</option>
            <option value="new">New</option>
          </Select>
        </Box>
      </Flex>

      {renderGridProduct}

      <Flex marginY="20px" justifyContent="center">
        <Pagination
          onPageChange={handlePageClick}
          pageRangeDisplayed={5}
          pageCount={pageCount}
          renderOnZeroPageCount={null}
        />
      </Flex>
    </Stack>
  );
};

export default ProductGrid;
