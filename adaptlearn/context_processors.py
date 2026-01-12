def shopowner_status(request):
  if request.user.is_authenticated:
    return {
      "is_shopowner" : request.user.groups.filter(name = "ShopOwner").exists()
    }
  return {"is_shopowner" : False}