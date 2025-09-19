from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from datetime import timedelta
from .models import Client
from .serializers import ClientSerializer

# Constants for better maintainability
DEFAULT_PAGE_SIZE = 15
MAX_PAGE_SIZE = 50
VALID_ORDERING_FIELDS = ['created_at', 'updated_at', 'first_name', 'other_names', 'phone', 'email']

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def client_list_create(request):
    if request.method == 'GET':
        return _get_client_list(request)
    elif request.method == 'POST':
        return _create_client(request)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def client_detail(request, pk):

    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'GET':
        return _get_client_detail(client)
    elif request.method in ['PUT', 'PATCH']:
        return _update_client(client, request, partial=request.method == 'PATCH')
    elif request.method == 'DELETE':
        return _delete_client(client)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def client_search(request):
    try:
        queryset = Client.objects.all()
        queryset = _apply_filters(queryset, request)
        queryset = _apply_search(queryset, request)
        queryset = _apply_ordering(queryset, request)
        
        # Pagination with validation
        page = request.query_params.get('page', 1)
        page_size = min(int(request.query_params.get('page_size', DEFAULT_PAGE_SIZE)), MAX_PAGE_SIZE)
        
        paginator = Paginator(queryset, page_size)
        
        try:
            clients = paginator.page(page)
        except PageNotAnInteger:
            clients = paginator.page(1)
        except EmptyPage:
            clients = paginator.page(paginator.num_pages)
        serializer = ClientSerializer(clients, many=True, context={'request': request})
        return Response({
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': clients.number,
            'page_size': page_size,
            'next': clients.next_page_number() if clients.has_next() else None,
            'previous': clients.previous_page_number() if clients.has_previous() else None,
            'results': serializer.data
        })
        
    except Exception as e:
        return Response(
            {"error": "An error occurred during search", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def client_stats(request):

    try:
        total_clients = Client.objects.count()
        user_clients = Client.objects.filter(credit_officer=request.user)
        my_clients = user_clients.count()
        recent_clients = Client.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        return Response({
            'total_clients': total_clients,
            'my_clients': my_clients,
            'recent_clients': recent_clients,
        })
        
    except Exception as e:
        return Response(
            {"error": "Failed to retrieve statistics", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def _get_client_list(request):
    try:
        queryset = Client.objects.all()
        credit_officer_id = request.query_params.get('credit_officer')
        if credit_officer_id:
            queryset = queryset.filter(credit_officer_id=credit_officer_id)
        ordering = request.query_params.get('ordering', '-created_at')
        if ordering.lstrip('-') in VALID_ORDERING_FIELDS:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('-created_at')
        
        # Pagination with validation
        page = request.query_params.get('page', 1)
        page_size = min(int(request.query_params.get('page_size', DEFAULT_PAGE_SIZE)), MAX_PAGE_SIZE)
        
        paginator = Paginator(queryset, page_size)
        try:
            clients = paginator.page(page)
        except PageNotAnInteger:
            clients = paginator.page(1)
        except EmptyPage:
            clients = paginator.page(paginator.num_pages)
        
        serializer = ClientSerializer(clients, many=True, context={'request': request})
        
        return Response({
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': clients.number,
            'page_size': page_size,
            'next': clients.next_page_number() if clients.has_next() else None,
            'previous': clients.previous_page_number() if clients.has_previous() else None,
            'results': serializer.data
        })
        
    except ValueError:
        return Response(
            {"error": "Invalid page or page_size parameter"},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": "Failed to retrieve client list", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def _create_client(request):
    # Create a new client with validation
    try:
        serializer = ClientSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response(
            {"error": "Failed to create client", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def _get_client_detail(client, request):
    try:
        serializer = ClientSerializer(client, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {"error": "Failed to retrieve client details", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def _update_client(client, request, partial=False):
    # Update a client with proper error handling
    try:
        serializer = ClientSerializer(
            client, 
            data=request.data, 
            partial=partial,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response(
            {"error": "Failed to update client", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def _delete_client(client):
    try:
        client.delete()
        return Response(
            {"message": "Client deleted successfully!"}, 
            status=status.HTTP_204_NO_CONTENT
        )
    except Exception as e:
        return Response(
            {"error": "Failed to delete client", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def _apply_filters(queryset, request):

    filters = {}
    if 'credit_officer' in request.query_params:
        filters['credit_officer_id'] = request.query_params['credit_officer']

    # Date range filters
    if 'created_after' in request.query_params:
        try:
            queryset = queryset.filter(created_at__gte=request.query_params['created_after'])
        except ValueError:
            pass 
    if 'created_before' in request.query_params:
        try:
            queryset = queryset.filter(created_at__lte=request.query_params['created_before'])
        except ValueError:
            pass    
    return queryset.filter(**filters) if filters else queryset

def _apply_search(queryset, request):
    # Apply search functionality across multiple fields
    search_term = request.query_params.get('search')
    
    if search_term:
        queryset = queryset.filter(
            Q(first_name__icontains=search_term) |
            Q(other_names__icontains=search_term) |
            Q(phone__icontains=search_term) |
            Q(email__icontains=search_term) |
            Q(national_id__icontains=search_term) |
            Q(passport_number__icontains=search_term) |
            Q(occupation__icontains=search_term) |
            Q(credit_officer__username__icontains=search_term) |
            Q(credit_officer__first_name__icontains=search_term) |
            Q(credit_officer__last_name__icontains=search_term)
        )
    return queryset

def _apply_ordering(queryset, request):
    """
    Apply ordering with validation
    """
    ordering = request.query_params.get('ordering', '-created_at')
    
    if ordering.lstrip('-') in VALID_ORDERING_FIELDS:
        return queryset.order_by(ordering)
    
    # Default ordering
    return queryset.order_by('-created_at')



