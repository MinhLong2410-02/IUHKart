import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import {
    Box,
    CloseButton,
    Flex,
    Text,
    Button,
    useDisclosure,
    Drawer,
    DrawerContent,
    useColorModeValue,
} from '@chakra-ui/react';
import Cookies from 'js-cookie'; // Import Cookies if using it for authentication

const LinkItems = [
    { path: "summary", name: 'Summary' },
    { path: "info", name: 'Info' },
    { path: "products", name: 'Products' },
];

export default function SimpleSidebar({ children }) {
    const { isOpen, onOpen, onClose } = useDisclosure();
    return (
        <Box minH="100vh">
            <SidebarContent onClose={() => onClose()} display={{ base: 'none', md: 'block' }} className='relative' />
            <Drawer
                autoFocus={false}
                isOpen={isOpen}
                placement="left"
                onClose={onClose}
                returnFocusOnClose={false}
                onOverlayClick={onClose}
                size="full">
                <DrawerContent>
                    <SidebarContent onClose={onClose} />
                </DrawerContent>
            </Drawer>
        </Box>
    );
}

const SidebarContent = ({ onClose, ...rest }) => {
    const navigate = useNavigate();

    const handleLogout = () => {
        // Clear authentication tokens
        Cookies.remove('authorization'); // If using cookies
        localStorage.removeItem('authorization'); // If using local storage
        // Redirect to login page
        navigate('/login');
    };

    return (
        <Box
            bg={"white"}
            borderRight="1px"
            borderRadius={20}
            borderRightColor={useColorModeValue('gray.200', 'gray.700')}
            w={{ base: 'full', md: 60 }}
            pos="fixed"
            h="80%"
            {...rest}>
            <Flex h="20" alignItems="center" mx="8" justifyContent="space-between">
                <Text fontSize="2xl" fontFamily="monospace" fontWeight="bold">
                    Logo
                </Text>
                <CloseButton display={{ base: 'flex', md: 'none' }} onClick={onClose} />
            </Flex>
            {LinkItems.map((link) => (
                <NavItem key={link.name} path={link.path}>
                    {link.name}
                </NavItem>
            ))}
            {/* Add Logout Button */}
            <Flex p="4" mt="auto" justifyContent="center">
                <Button colorScheme="red" onClick={handleLogout}>
                    Log Out
                </Button>
            </Flex>
        </Box>
    );
};

const NavItem = ({ icon, children, path, ...rest }) => {
    return (
        <Link to={path} style={{ textDecoration: 'none' }} _focus={{ boxShadow: 'none' }}>
            <Flex
                align="center"
                p="4"
                mx="4"
                borderRadius="lg"
                role="group"
                cursor="pointer"
                bg={useLocation().pathname === `/${path}` ? 'cyan.400' : 'white'}
                _hover={{
                    bg: 'cyan.400',
                    color: 'white',
                }}
                {...rest}>
                {icon && (
                    <Icon
                        mr="4"
                        fontSize="16"
                        _groupHover={{
                            color: 'white',
                        }}
                        as={icon}
                    />
                )}
                {children}
            </Flex>
        </Link>
    );
};
