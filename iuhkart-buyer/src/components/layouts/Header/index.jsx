import { useCallback, useContext, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Button,
  Flex,
  Heading,
  Image,
  Input,
  Stack,
  Text,
} from "@chakra-ui/react";
import { Icon } from "@iconify/react";

import logoSVG from "../../../assets/images/logo.svg";
import collectionAPI from "../../../api/collection.api";
import _, { isEmpty } from "lodash";
import { GlobalContext } from "../../../contexts/GlobalContext";

const Header = () => {
  const navigate = useNavigate();

  const { setProductID } = useContext(GlobalContext);

  const [searchActive, setSearchActive] = useState(false);
  const [searchResults, setSearchResults] = useState([]);

  const toggleSearch = () => {
    setSearchActive((prev) => !prev);
  };

  const handleLiveSearch = async (event) => {
    const value = event.target.value;

    if (!value.trim()) {
      setSearchResults([]);
      return;
    }

    const response = await collectionAPI.search(value);
    const data = response.data;

    setSearchResults(data?.results);
  };

  const handleBlurSearch = () => {
    setSearchResults([]);
    setSearchActive(false);
  };

  const handleClickProduct = useCallback(
    (result) => {
      setProductID(result.payload["product_id"]);
      setSearchActive(false);
      navigate(`/products/${result.payload["product_id"]}`);
    },
    [navigate, setProductID]
  );

  const debounceLiveSearch = _.debounce(handleLiveSearch, 300);

  const renderSearchView = useMemo(() => {
    return (
      <Box height="100%" position="relative">
        <Box>
          <Input
            placeholder="Search"
            onChange={debounceLiveSearch}
            onBlur={handleBlurSearch}
          />
        </Box>
        {!isEmpty(searchResults) && (
          <Stack
            width="500px"
            height="500px"
            position="absolute"
            right={0}
            backgroundColor="white"
            overflowY="scroll"
            zIndex={99999999}
          >
            {searchResults.map((result) => (
              <Flex
                alignItems="center"
                _hover={{ cursor: "pointer" }}
                onClick={() => handleClickProduct(result)}
              >
                <Box>
                  <Image src={result.payload.product_image_url} />
                </Box>
                <Box padding="25px">
                  <Heading as="h6" size="xs" noOfLines={1}>
                    {result.payload.product_name}
                  </Heading>
                </Box>
              </Flex>
            ))}
          </Stack>
        )}
      </Box>
    );
  }, [debounceLiveSearch]);

  return (
    <Flex
      width="100%"
      paddingY="20px"
      paddingX="5%"
      // position="fixed"
      justifyContent="space-between"
      alignItems="center"
      borderBottom="1px solid #E6E6E6"
      backgroundColor="transparent"
      textColor="#3734a9"
    >
      <Flex>
        <Box
          width="300px"
          _hover={{
            cursor: "pointer",
          }}
          onClick={() => navigate("/")}
        >
          <Image height="52px" src={logoSVG} />
        </Box>
      </Flex>
      <Flex gap={10} fontWeight={600}>
        <Text>Home</Text>
        <Text>Products</Text>
        <Text>Contact</Text>
      </Flex>
      <Flex fontWeight={600} gap={5}>
        <Box>
          {!searchActive ? (
            <Button
              size="lg"
              variant="ghost"
              leftIcon={<Icon icon="tabler:search" />}
              paddingX="10px"
              borderRadius="20px"
              textColor="#3734a9"
              onClick={toggleSearch}
            >
              Search
            </Button>
          ) : (
            renderSearchView
          )}
        </Box>
        <Box>
          <Button
            size="lg"
            variant="ghost"
            leftIcon={<Icon icon="vaadin:cart-o" />}
            paddingX="10px"
            borderRadius="20px"
            textColor="#3734a9"
            onClick={() => navigate("/cart")}
          >
            Cart
          </Button>
        </Box>
        <Box>
          <Button
            size="lg"
            backgroundColor="#3734a9"
            borderRadius="20px"
            textColor="white"
            _hover={{
              backgroundColor: "#333190",
            }}
          >
            Get started
          </Button>
        </Box>
      </Flex>
    </Flex>
  );
};

export default Header;
