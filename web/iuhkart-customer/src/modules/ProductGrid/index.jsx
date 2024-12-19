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
  const [productDataSet, setProductDataSet] = useState({ results: [] });
  const [productDataSetRecommend, setProductDataSetRecommend] = useState([]);
  const [pageCount, setPageCount] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  // const [showAll, setShowAll] = useState(false);
  const [visibleCount, setVisibleCount] = useState(4); // Hiển thị 4 sản phẩm mặc định

  // Fetch product data and recommendations
  useEffect(() => {
    const getProducts = async () => {
      try {
        setLoading(true);

        const data = await productApi.getProducts(
          categorySelected,
          currentPage,
          PRODUCT_PAGING.pageSize
        );

        const dataRecommend = await productApi.getProductRecommend();

        setProductDataSet(data || { results: [] });
        setProductDataSetRecommend(Array.isArray(dataRecommend) ? dataRecommend : []);
        setPageCount(Math.ceil((data?.count || 0) / PRODUCT_PAGING.pageSize));
      } catch (error) {
        console.error("Error fetching products:", error);
      } finally {
        setLoading(false);
      }
    };

    getProducts();
  }, [categorySelected, currentPage]);

  // Handle pagination
  const handlePageClick = async (data) => {
    setCurrentPage(data?.selected + 1 || 1);
  };

  // Handle product click
  const handleClickProduct = useCallback(
    (product) => {
      setProductID(product?.product_id);
      navigate(`/products/${product?.product_id}`);
    },
    [navigate, setProductID]
  );

  // Handle add to cart
  const handleAddCart = useCallback(
    async (productID) => {
      try {
        const payload = { product: productID, quantity: 1 };
        const data = await cartAPI.addProduct(payload);

        if (!_.isEmpty(data)) {
          toast({
            title: "Add Cart Successful!",
            status: "success",
            position: "top-left",
          });
        }
      } catch (error) {
        toast({
          title: "Add Cart Fail!",
          status: "error",
          position: "top-left",
        });
      }
    },
    [toast]
  );

  // Render grid of recommended products
  const renderGridProductRecommend = useMemo(() => {
    const displayedProducts = productDataSetRecommend.slice(0, visibleCount);

    return (
      <>
        {isLoading ? (
          <Flex justifyContent="center">
            <Spinner size="xl" color="#3734a9" />
          </Flex>
        ) : (
          <>
            <Grid templateColumns="repeat(4, 1fr)" gap={5}>
              {!_.isEmpty(displayedProducts) &&
                displayedProducts.map((product, index) => (
                  <GridItem key={index}>
                    <ProductCard
                      product={product}
                      onAddCart={handleAddCart}
                      onClick={handleClickProduct}
                    />
                  </GridItem>
                ))}
            </Grid>
            {visibleCount < productDataSetRecommend.length && (
              <Flex justifyContent="center" mt={4}>
                <Text
                  as="button"
                  fontWeight="bold"
                  color="#3734a9"
                  onClick={() => setVisibleCount((prev) => prev + 4)}
                >
                  Xem thêm
                </Text>
              </Flex>
            )}
          </>
        )}
      </>
    );
  }, [isLoading, productDataSetRecommend, handleAddCart, handleClickProduct, visibleCount]);

  // Render grid of products with pagination
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
                <GridItem key={index}>
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
      {/* Recommended Products */}
      { productDataSetRecommend?.length > 0  && <>
        <Flex marginBottom="15px" justifyContent="space-between">
          <Flex alignItems="center" gap={3}>
            <Heading as="h3" size="lg">
              Dành cho bạn
            </Heading>
          </Flex>
        </Flex>
        {renderGridProductRecommend}
      </>}

      <br />

      {/* Main Product Grid */}
      <Flex marginBottom="15px" marginTop={"30px"} justifyContent="space-between">
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

      {/* Pagination */}
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
